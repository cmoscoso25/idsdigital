from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .forms import DemoRequestForm
from .models import DemoRequest


def _get_client_ip(request) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_http_methods(["GET"])
def landing(request):
    ok = request.GET.get("ok") == "1"
    form = DemoRequestForm()
    return render(request, "public/landing.html", {"form": form, "ok": ok})


@require_http_methods(["POST"])
def submit_demo_request(request):
    form = DemoRequestForm(request.POST)

    if not form.is_valid():
        return render(request, "public/landing.html", {"form": form, "ok": False}, status=400)

    cd = form.cleaned_data

    DemoRequest.objects.create(
        name=cd["nombre"],
        email=cd["email"],
        phone=cd.get("telefono", "") or "",
        company=cd.get("empresa", "") or "",
        subject=cd.get("asunto", "") or "",
        message=cd.get("mensaje", "") or "",
        submitted_ip=_get_client_ip(request),
        user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:255],
    )

    return redirect(f"{reverse('public:landing')}?ok=1")


@require_http_methods(["GET"])
def services(request):
    return render(request, "public/services.html")


@require_http_methods(["GET"])
def automation_processes(request):
    return render(request, "public/automatizacion_procesos.html")


@require_http_methods(["GET"])
def custom_software_development(request):
    return render(request, "public/desarrollo_software_medida.html")


@require_http_methods(["GET"])
def ai_solutions(request):
    return render(request, "public/inteligencia_artificial_empresas.html")


def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /panel/
Disallow: /accounts/
Disallow: /core/

Sitemap: https://ids.cl/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")