"""
Servicio de generación de imágenes IA para creatividades Instagram.

Flujo: prompt_visual → API IA → descarga PNG → MEDIA_ROOT → imagen_generada

Proveedor activo:   fal  (Flux Pro via fal-client)
Preparados:         openai, ideogram, gemini  (retornan error controlado)

Para agregar un proveedor: implementar _generar_con_<nombre>(prompt, tipo) → str (URL)
y registrarlo en _PROVEEDORES.

Variables de entorno:
  FAL_KEY              — requerida para proveedor "fal"
  NEXA_IMAGE_PROVIDER  — proveedor por defecto (default: "fal")
  NEXA_FAL_MODEL       — modelo Fal AI (default: "fal-ai/flux-pro")
"""
import os
import uuid
import requests
from pathlib import Path
from django.conf import settings


# ── Helpers privados ──────────────────────────────────────────────────────────

def _ruta_guardado(creatividad_pk: int, extension: str = "png") -> tuple[Path, str]:
    carpeta = Path(settings.MEDIA_ROOT) / "nexa" / "creatividades"
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = f"creatividad_{creatividad_pk}_{uuid.uuid4().hex[:8]}.{extension}"
    return carpeta / nombre, f"nexa/creatividades/{nombre}"


def _descargar(url: str, ruta_abs: Path) -> None:
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    ruta_abs.write_bytes(respuesta.content)


def _imagen_size_fal(tipo: str) -> str:
    """Mapea tipo de creatividad al image_size de Fal AI."""
    return "portrait_4_3" if tipo == "historia" else "square_hd"


# ── Proveedores ───────────────────────────────────────────────────────────────

def _generar_con_fal(prompt: str, tipo: str) -> str:
    """
    Llama a Fal AI (Flux Pro) y devuelve la URL de la imagen generada.
    Requiere FAL_KEY en entorno o settings.FAL_KEY.
    """
    import fal_client

    fal_key = getattr(settings, "FAL_KEY", "") or os.environ.get("FAL_KEY", "")
    if not fal_key:
        raise ValueError(
            "FAL_KEY no está configurada. "
            "Agrega la variable de entorno FAL_KEY para usar Flux."
        )

    os.environ["FAL_KEY"] = fal_key  # fal_client la lee del entorno

    modelo = getattr(settings, "NEXA_FAL_MODEL", "fal-ai/flux-pro")
    size = _imagen_size_fal(tipo)

    resultado = fal_client.run(
        modelo,
        arguments={
            "prompt": prompt[:2000],
            "image_size": size,
            "num_images": 1,
            "safety_tolerance": "2",
        },
    )

    imagenes = resultado.get("images", [])
    if not imagenes:
        raise ValueError("Fal AI no devolvió imágenes en la respuesta")

    return imagenes[0]["url"]


def _generar_con_openai(prompt: str, tipo: str) -> str:
    """Llama a OpenAI DALL-E 2. Requiere OPENAI_API_KEY en entorno."""
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está configurada en el entorno")

    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.images.generate(
        model="dall-e-2",
        prompt=prompt[:1000],
        n=1,
        size="1024x1024",
    )
    return respuesta.data[0].url


def _generar_con_ideogram(prompt: str, tipo: str) -> str:
    raise NotImplementedError("Integración con Ideogram aún no implementada")


def _generar_con_gemini(prompt: str, tipo: str) -> str:
    raise NotImplementedError("Integración con Gemini Imagen aún no implementada")


# ── Dispatcher ────────────────────────────────────────────────────────────────

_PROVEEDORES = {
    "fal":      _generar_con_fal,
    "openai":   _generar_con_openai,
    "ideogram": _generar_con_ideogram,
    "gemini":   _generar_con_gemini,
}

PROVEEDORES_DISPONIBLES = list(_PROVEEDORES.keys())


def generar_imagen_para_creatividad(
    creatividad,
    proveedor: str | None = None,
) -> dict:
    """
    Genera imagen IA, la descarga y guarda en MEDIA_ROOT.

    Args:
        creatividad: instancia de CreatividadInstagram
        proveedor:   "fal" | "openai" | "ideogram" | "gemini"
                     Si None, usa settings.NEXA_IMAGE_PROVIDER (default "fal")

    Returns:
        {"ok": True,  "ruta": str, "proveedor": str}
        {"ok": False, "error": str}
    """
    if proveedor is None:
        proveedor = getattr(settings, "NEXA_IMAGE_PROVIDER", "fal")

    prompt = (creatividad.prompt_visual or "").strip()
    if not prompt:
        return {"ok": False, "error": "La creatividad no tiene prompt visual configurado"}

    fn = _PROVEEDORES.get(proveedor)
    if fn is None:
        return {"ok": False, "error": f"Proveedor '{proveedor}' no reconocido"}

    try:
        url_imagen = fn(prompt, creatividad.tipo)
        extension = "jpg" if "jpeg" in url_imagen.lower() or "jpg" in url_imagen.lower() else "png"
        ruta_abs, ruta_relativa = _ruta_guardado(creatividad.pk, extension)
        _descargar(url_imagen, ruta_abs)
        return {"ok": True, "ruta": ruta_relativa, "proveedor": proveedor}

    except NotImplementedError as exc:
        return {"ok": False, "error": str(exc)}
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# Alias conveniente para import directo desde shell / tests
def generar_imagen_fal(creatividad) -> dict:
    """Shortcut: genera imagen forzando proveedor 'fal'."""
    return generar_imagen_para_creatividad(creatividad, proveedor="fal")
