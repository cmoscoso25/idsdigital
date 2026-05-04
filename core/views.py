from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

try:
    from public.models import DemoRequest
except Exception:
    DemoRequest = None


def home(request):
    return render(request, "core/home.html")


def health_check(request):
    """
    Endpoint liviano para UptimeRobot / Render.
    No carga templates ni consulta datos pesados.
    Sirve para mantener activo el servicio y verificar disponibilidad.
    URL recomendada:
    /health/
    """
    return HttpResponse("OK", content_type="text/plain", status=200)


@csrf_exempt
@require_http_methods(["POST"])
def api_crear_solicitud(request):
    """
    Endpoint público para recibir solicitudes desde la landing.
    Acepta POST tipo form-data o x-www-form-urlencoded.
    """

    if DemoRequest is None:
        return JsonResponse(
            {"ok": False, "error": "Modelo DemoRequest no disponible."},
            status=500,
        )

    nombre = (request.POST.get("nombre") or "").strip()
    email = (request.POST.get("email") or "").strip()
    telefono = (request.POST.get("telefono") or "").strip()
    empresa = (request.POST.get("empresa") or "").strip()
    asunto = (request.POST.get("asunto") or "").strip()
    mensaje = (request.POST.get("mensaje") or "").strip()
    website = (request.POST.get("website") or "").strip()  # honeypot anti-spam

    if website:
        return JsonResponse({"ok": True, "spam": True}, status=200)

    if not nombre:
        return JsonResponse(
            {"ok": False, "error": "El nombre es obligatorio."},
            status=400,
        )

    if not email:
        return JsonResponse(
            {"ok": False, "error": "El email es obligatorio."},
            status=400,
        )

    try:
        # Compatibilidad con modelos en español o inglés
        create_kwargs = {}

        model_fields = {field.name for field in DemoRequest._meta.fields}

        if "nombre" in model_fields:
            create_kwargs["nombre"] = nombre
        elif "name" in model_fields:
            create_kwargs["name"] = nombre

        if "email" in model_fields:
            create_kwargs["email"] = email

        if "telefono" in model_fields:
            create_kwargs["telefono"] = telefono
        elif "phone" in model_fields:
            create_kwargs["phone"] = telefono

        if "empresa" in model_fields:
            create_kwargs["empresa"] = empresa
        elif "company" in model_fields:
            create_kwargs["company"] = empresa

        if "asunto" in model_fields:
            create_kwargs["asunto"] = asunto
        elif "subject" in model_fields:
            create_kwargs["subject"] = asunto

        if "mensaje" in model_fields:
            create_kwargs["mensaje"] = mensaje
        elif "message" in model_fields:
            create_kwargs["message"] = mensaje

        # Estado inicial si existe en el modelo
        if "status" in model_fields:
            create_kwargs["status"] = "new"

        obj = DemoRequest.objects.create(**create_kwargs)

        return JsonResponse(
            {
                "ok": True,
                "message": "Solicitud creada correctamente.",
                "id": obj.id,
            },
            status=201,
        )

    except Exception as e:
        return JsonResponse(
            {"ok": False, "error": f"No se pudo guardar la solicitud: {str(e)}"},
            status=500,
        )