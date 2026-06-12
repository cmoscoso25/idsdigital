import json
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from billing.models import Plan, Subscription

logger = logging.getLogger("billing")


def _get_or_create_subscription(usuario):
    sub, created = Subscription.objects.get_or_create(
        usuario=usuario,
        defaults={
            "estado": Subscription.TRIAL,
            "trial_fin": timezone.now() + timezone.timedelta(days=14),
        },
    )
    return sub


@login_required
def billing_dashboard(request):
    sub = _get_or_create_subscription(request.user)
    planes = Plan.objects.filter(activo=True)
    return render(request, "nexa/billing.html", {
        "subscription": sub,
        "planes": planes,
        "stripe_pub_key": settings.STRIPE_PUBLISHABLE_KEY,
    })


@login_required
def checkout_redirect(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, activo=True)

    if not plan.stripe_price_id:
        messages.error(request, "Este plan no está disponible aún para pago. Contacta a soporte.")
        return redirect("billing:dashboard")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    sub = _get_or_create_subscription(request.user)

    if not sub.stripe_customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.get_full_name() or request.user.email,
            metadata={"usuario_id": str(request.user.id)},
        )
        sub.stripe_customer_id = customer.id
        sub.save(update_fields=["stripe_customer_id"])

    base_url = request.build_absolute_uri("/").rstrip("/")
    session = stripe.checkout.Session.create(
        customer=sub.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        mode="subscription",
        success_url=f"{base_url}/nexa/app/billing/exito/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/nexa/app/billing/cancelar/",
        metadata={"usuario_id": str(request.user.id), "plan_id": str(plan.id)},
        allow_promotion_codes=True,
    )
    return redirect(session.url, permanent=False)


@login_required
def checkout_success(request):
    session_id = request.GET.get("session_id", "")
    return render(request, "nexa/billing_exito.html", {"session_id": session_id})


@login_required
def checkout_cancel(request):
    messages.info(request, "Cancelaste el proceso de pago. Puedes intentarlo de nuevo cuando quieras.")
    return redirect("billing:dashboard")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (stripe.error.SignatureVerificationError, ValueError) as e:
        logger.warning("Webhook inválido: %s", e)
        return HttpResponse(status=400)

    _procesar_evento(event)
    return HttpResponse(status=200)


def _procesar_evento(event):
    data = event["data"]["object"]
    tipo = event["type"]

    if tipo == "checkout.session.completed":
        _activar_suscripcion(data)

    elif tipo in ("customer.subscription.updated", "customer.subscription.created"):
        _sincronizar_suscripcion(data)

    elif tipo == "customer.subscription.deleted":
        _cancelar_suscripcion(data)

    elif tipo == "invoice.payment_failed":
        _marcar_pago_fallido(data)


def _activar_suscripcion(session):
    usuario_id = session.get("metadata", {}).get("usuario_id")
    plan_id = session.get("metadata", {}).get("plan_id")
    stripe_sub_id = session.get("subscription", "")

    if not usuario_id or not plan_id:
        logger.error("checkout.session.completed sin metadata usuario_id/plan_id")
        return

    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        usuario = User.objects.get(id=usuario_id)
        plan = Plan.objects.get(id=plan_id)
    except Exception as e:
        logger.error("Error al activar suscripción: %s", e)
        return

    sub, _ = Subscription.objects.get_or_create(usuario=usuario)
    sub.plan = plan
    sub.estado = Subscription.ACTIVO
    sub.stripe_subscription_id = stripe_sub_id
    sub.save(update_fields=["plan", "estado", "stripe_subscription_id"])
    logger.info("Suscripción activada: usuario=%s plan=%s", usuario_id, plan.nombre)


def _sincronizar_suscripcion(stripe_sub):
    stripe_sub_id = stripe_sub.get("id", "")
    stripe_status = stripe_sub.get("status", "")
    period_end = stripe_sub.get("current_period_end")

    try:
        sub = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
    except Subscription.DoesNotExist:
        return

    estado_map = {
        "active": Subscription.ACTIVO,
        "past_due": Subscription.PAGO_FALLIDO,
        "canceled": Subscription.CANCELADO,
        "unpaid": Subscription.PAGO_FALLIDO,
    }
    sub.estado = estado_map.get(stripe_status, sub.estado)
    if period_end:
        sub.periodo_actual_fin = timezone.datetime.fromtimestamp(period_end, tz=timezone.utc)
    sub.save(update_fields=["estado", "periodo_actual_fin"])


def _cancelar_suscripcion(stripe_sub):
    stripe_sub_id = stripe_sub.get("id", "")
    try:
        sub = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
        sub.estado = Subscription.CANCELADO
        sub.save(update_fields=["estado"])
        logger.info("Suscripción cancelada: stripe_sub=%s", stripe_sub_id)
    except Subscription.DoesNotExist:
        pass


def _marcar_pago_fallido(invoice):
    stripe_sub_id = invoice.get("subscription", "")
    if not stripe_sub_id:
        return
    try:
        sub = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
        sub.estado = Subscription.PAGO_FALLIDO
        sub.save(update_fields=["estado"])
        logger.warning("Pago fallido: stripe_sub=%s usuario=%s", stripe_sub_id, sub.usuario_id)
    except Subscription.DoesNotExist:
        pass
