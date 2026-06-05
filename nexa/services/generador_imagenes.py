"""
Servicio de generación de imágenes IA para creatividades Instagram.

Flujo: prompt_visual → API IA → descarga PNG → MEDIA_ROOT → imagen_generada

Proveedores soportados hoy:  openai (DALL-E 3)
Proveedores preparados:      flux, ideogram, gemini  (retornan error controlado)

Para agregar un nuevo proveedor: implementar _generar_con_<proveedor>(prompt, **kwargs)
y agregarlo al dispatcher en generar_imagen_para_creatividad().
"""
import os
import uuid
import requests
from pathlib import Path
from django.conf import settings


# ── Helpers privados ──────────────────────────────────────────────────────────

def _ruta_guardado(creatividad_pk: int, extension: str = "png") -> tuple[Path, str]:
    """Devuelve (ruta_absoluta, ruta_relativa_a_MEDIA_ROOT)."""
    carpeta = Path(settings.MEDIA_ROOT) / "nexa" / "creatividades"
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = f"creatividad_{creatividad_pk}_{uuid.uuid4().hex[:8]}.{extension}"
    return carpeta / nombre, f"nexa/creatividades/{nombre}"


def _descargar(url: str, ruta_abs: Path) -> None:
    """Descarga una URL y escribe en disco."""
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    ruta_abs.write_bytes(respuesta.content)


# ── Proveedores ───────────────────────────────────────────────────────────────

def _generar_con_openai(prompt: str, tipo: str) -> str:
    """
    Llama a OpenAI DALL-E 3 y devuelve la URL temporal de la imagen.
    Requiere: OPENAI_API_KEY en entorno.
    """
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está configurada en el entorno")

    # Historia usa ratio 9:16; el resto cuadrado
    size = "1024x1792" if tipo == "historia" else "1024x1024"

    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.images.generate(
        model="dall-e-3",
        prompt=prompt[:4000],   # límite de la API
        n=1,
        size=size,
        quality="standard",
    )
    return respuesta.data[0].url


def _generar_con_flux(prompt: str, tipo: str) -> str:
    raise NotImplementedError("Integración con Flux aún no implementada")


def _generar_con_ideogram(prompt: str, tipo: str) -> str:
    raise NotImplementedError("Integración con Ideogram aún no implementada")


def _generar_con_gemini(prompt: str, tipo: str) -> str:
    raise NotImplementedError("Integración con Gemini Imagen aún no implementada")


# ── API pública ───────────────────────────────────────────────────────────────

_PROVEEDORES = {
    "openai":   _generar_con_openai,
    "flux":     _generar_con_flux,
    "ideogram": _generar_con_ideogram,
    "gemini":   _generar_con_gemini,
}

PROVEEDORES_DISPONIBLES = list(_PROVEEDORES.keys())


def generar_imagen_para_creatividad(
    creatividad,
    proveedor: str = "openai",
) -> dict:
    """
    Genera una imagen IA para la creatividad, la descarga y guarda en MEDIA_ROOT.

    Args:
        creatividad: instancia de CreatividadInstagram
        proveedor:   "openai" | "flux" | "ideogram" | "gemini"

    Returns:
        {"ok": True,  "ruta": str, "proveedor": str}
        {"ok": False, "error": str}
    """
    prompt = (creatividad.prompt_visual or "").strip()
    if not prompt:
        return {"ok": False, "error": "La creatividad no tiene prompt visual configurado"}

    fn_proveedor = _PROVEEDORES.get(proveedor)
    if fn_proveedor is None:
        return {"ok": False, "error": f"Proveedor '{proveedor}' no reconocido"}

    try:
        url_temporal = fn_proveedor(prompt, creatividad.tipo)
        ruta_abs, ruta_relativa = _ruta_guardado(creatividad.pk)
        _descargar(url_temporal, ruta_abs)
        return {"ok": True, "ruta": ruta_relativa, "proveedor": proveedor}

    except NotImplementedError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
