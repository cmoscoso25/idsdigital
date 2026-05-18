from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .forms import DemoRequestForm
from .models import DemoRequest, BlogPost
from .services.email_service import enviar_bienvenida_solicitud, enviar_notificacion_interna


def _get_client_ip(request) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_http_methods(["GET"])
def landing(request):
    ok = request.GET.get("ok") == "1"
    form = DemoRequestForm()
    # Traemos los artículos destacados para mostrar en la landing
    posts_destacados = BlogPost.objects.filter(published=True, featured=True)[:3]
    return render(request, "public/landing.html", {
        "form": form,
        "ok": ok,
        "posts_destacados": posts_destacados,
    })


@require_http_methods(["POST"])
def submit_demo_request(request):
    form = DemoRequestForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "public/landing.html",
            {"form": form, "ok": False},
            status=400,
        )

    cd = form.cleaned_data

    # Guardamos la solicitud en la base de datos
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

    # Le avisamos al lead que recibimos su solicitud
    enviar_bienvenida_solicitud(
        name=cd["nombre"],
        email=cd["email"],
        subject=cd.get("asunto", "") or "",
    )

    # Nos avisamos internamente para gestionar el lead rápido
    enviar_notificacion_interna(
        name=cd["nombre"],
        email=cd["email"],
        company=cd.get("empresa", "") or "",
        subject=cd.get("asunto", "") or "",
        message=cd.get("mensaje", "") or "",
    )

    return redirect(f"{reverse('public:landing')}?ok=1")


@require_http_methods(["GET"])
def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    return render(request, "public/blog.html", {"posts": posts})


@require_http_methods(["GET"])
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    # Traemos otros artículos relacionados excluyendo el actual
    posts_relacionados = BlogPost.objects.filter(
        published=True
    ).exclude(slug=slug)[:3]
    return render(request, "public/blog_detail.html", {
        "post": post,
        "posts_relacionados": posts_relacionados,
    })


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


@require_http_methods(["GET"])
def software_empresas_chile(request):
    return render(request, "public/software_empresas_chile.html")


@require_http_methods(["GET"])
def sistemas_gestion_empresarial_chile(request):
    return render(request, "public/sistemas_gestion_empresarial_chile.html")


@require_http_methods(["GET"])
def automatizacion_python_empresas(request):
    return render(request, "public/automatizacion_python_empresas.html")


@require_http_methods(["GET"])
def dashboards_empresariales_chile(request):
    return render(request, "public/dashboards_empresariales_chile.html")


@require_http_methods(["GET"])
def inteligencia_artificial_empresas_chile(request):
    return render(request, "public/inteligencia_artificial_empresas_chile.html")


@require_http_methods(["GET"])
def desarrollo_sistemas_internos(request):
    return render(request, "public/desarrollo_sistemas_internos.html")


@require_http_methods(["GET", "HEAD"])
def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /panel/
Disallow: /accounts/
Disallow: /core/

Sitemap: https://www.idsdigital.cl/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")