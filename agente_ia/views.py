import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from public.models import DemoRequest

from .models import ConversacionAgente, MensajeAgente
from .services import generar_diagnostico_ia


def obtener_ip_cliente(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")

    if xff:
        return xff.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")


@csrf_exempt
@require_POST
def chat_diagnostico(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "ok": False,
                "error": "Solicitud inválida.",
            },
            status=400,
        )

    mensajes = data.get("mensajes", [])

    if not isinstance(mensajes, list):
        return JsonResponse(
            {
                "ok": False,
                "error": "Formato de mensajes inválido.",
            },
            status=400,
        )

    respuesta = generar_diagnostico_ia(mensajes)

    conversacion_id = data.get("conversacion_id")

    conversacion = None

    if conversacion_id:
        conversacion = ConversacionAgente.objects.filter(id=conversacion_id).first()

    if not conversacion:
        conversacion = ConversacionAgente.objects.create(
            ip=obtener_ip_cliente(request),
        )

    ultimo_mensaje_usuario = ""

    for mensaje in reversed(mensajes):
        if mensaje.get("role") == "user":
            ultimo_mensaje_usuario = mensaje.get("content", "").strip()
            break

    if ultimo_mensaje_usuario:
        MensajeAgente.objects.create(
            conversacion=conversacion,
            rol="user",
            mensaje=ultimo_mensaje_usuario,
        )

    MensajeAgente.objects.create(
        conversacion=conversacion,
        rol="assistant",
        mensaje=respuesta,
    )

    return JsonResponse(
        {
            "ok": True,
            "respuesta": respuesta,
            "conversacion_id": conversacion.id,
        }
    )


@csrf_exempt
@require_POST
def guardar_diagnostico(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "ok": False,
                "error": "Solicitud inválida.",
            },
            status=400,
        )

    nombre = (data.get("nombre") or "").strip()
    empresa = (data.get("empresa") or "").strip()
    email = (data.get("email") or "").strip()
    telefono = (data.get("telefono") or "").strip()
    resumen = (data.get("resumen") or "").strip()
    conversacion_id = data.get("conversacion_id")

    if not nombre or not email:
        return JsonResponse(
            {
                "ok": False,
                "error": "Nombre y correo son obligatorios.",
            },
            status=400,
        )

    conversacion = None

    if conversacion_id:
        conversacion = ConversacionAgente.objects.filter(id=conversacion_id).first()

    if conversacion:
        conversacion.nombre = nombre
        conversacion.empresa = empresa
        conversacion.correo = email
        conversacion.telefono = telefono
        conversacion.save(
            update_fields=[
                "nombre",
                "empresa",
                "correo",
                "telefono",
            ]
        )

    mensaje = f"""
Solicitud generada desde el Agente IA de IDS Digital.

Resumen de conversación:
{resumen}
""".strip()

    DemoRequest.objects.create(
        name=nombre,
        email=email,
        phone=telefono,
        company=empresa,
        subject="Diagnóstico Digital con Agente IA",
        message=mensaje,
        submitted_ip=obtener_ip_cliente(request),
        user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:255],
    )

    return JsonResponse(
        {
            "ok": True,
            "mensaje": "Diagnóstico guardado correctamente.",
        }
    )