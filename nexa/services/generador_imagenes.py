"""
Servicio de generación de imágenes para creatividades Instagram.

Proveedores:
  internal  — motor visual propio (HTML/CSS/SVG). Sin costo, sin API externa. DEFAULT.
  fal       — Fal AI / Flux Pro. Premium. Requiere FAL_KEY + saldo.
  openai    — OpenAI DALL-E. Premium. Requiere OPENAI_API_KEY + saldo.
  ideogram  — Ideogram. Premium. Stub preparado.
  gemini    — Gemini Imagen. Premium. Stub preparado.

Variables de entorno opcionales (solo para proveedores premium):
  FAL_KEY, OPENAI_API_KEY
  NEXA_IMAGE_PROVIDER  (default: "internal")
  NEXA_FAL_MODEL       (default: "fal-ai/flux-pro")
"""
import os
import uuid
import requests
from pathlib import Path
from django.conf import settings

PROVEEDORES_PREMIUM = {"fal", "openai", "ideogram", "gemini"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ruta_guardado(creatividad_pk: int, extension: str = "png") -> tuple[Path, str]:
    carpeta = Path(settings.MEDIA_ROOT) / "nexa" / "creatividades"
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = f"creatividad_{creatividad_pk}_{uuid.uuid4().hex[:8]}.{extension}"
    return carpeta / nombre, f"nexa/creatividades/{nombre}"


def _descargar(url: str, ruta_abs: Path) -> None:
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    ruta_abs.write_bytes(respuesta.content)


# ── Proveedor interno (sin costo, sin API) ────────────────────────────────────

def _generar_con_internal(creatividad) -> dict:
    """
    Motor visual interno. Usa render_html/render_css ya generados.
    No llama ninguna API externa. No requiere créditos ni claves.
    Devuelve resultado especial sin archivo de imagen.
    """
    if not creatividad.render_html:
        return {
            "ok": False,
            "error": "Esta creatividad no tiene render HTML. Usa 'Regenerar' para generarlo.",
        }
    return {"ok": True, "ruta": None, "proveedor": "internal", "interno": True}


# ── Proveedores premium ───────────────────────────────────────────────────────

def _generar_con_fal(prompt: str, tipo: str) -> str:
    import fal_client
    import logging

    fal_key = getattr(settings, "FAL_KEY", "")
    logging.getLogger(__name__).debug("FAL_KEY presente: %s", bool(fal_key))

    if not fal_key:
        raise ValueError(
            "FAL_KEY no está configurada en settings. "
            "Reinicia el servidor con la variable de entorno FAL_KEY establecida."
        )

    os.environ["FAL_KEY"] = fal_key
    modelo = getattr(settings, "NEXA_FAL_MODEL", "fal-ai/flux-pro")
    size = "portrait_4_3" if tipo == "historia" else "square_hd"

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

PROVEEDORES_DISPONIBLES = ["internal", "fal", "openai", "ideogram", "gemini"]

_MSG_PREMIUM = (
    "La generación IA externa es una opción premium. "
    "Actualmente estás usando el motor visual interno sin costo."
)


def generar_imagen_para_creatividad(creatividad, proveedor: str | None = None) -> dict:
    """
    Genera/renderiza creatividad según el proveedor.

    Proveedor "internal" (default): usa render_html existente, sin API ni costo.
    Proveedores premium: llaman API externa, requieren créditos y claves.

    Returns:
        {"ok": True,  "ruta": str|None, "proveedor": str, "interno": bool}
        {"ok": False, "error": str, "es_premium": bool}
    """
    if proveedor is None:
        proveedor = getattr(settings, "NEXA_IMAGE_PROVIDER", "internal")

    # Motor interno — no requiere prompt ni API
    if proveedor == "internal":
        return _generar_con_internal(creatividad)

    # Proveedores premium — requieren prompt visual
    if proveedor not in PROVEEDORES_PREMIUM:
        return {"ok": False, "error": f"Proveedor '{proveedor}' no reconocido", "es_premium": False}

    prompt = (creatividad.prompt_visual or "").strip()
    if not prompt:
        return {"ok": False, "error": "La creatividad no tiene prompt visual configurado", "es_premium": False}

    fn_map = {
        "fal":      lambda: _generar_con_fal(prompt, creatividad.tipo),
        "openai":   lambda: _generar_con_openai(prompt, creatividad.tipo),
        "ideogram": lambda: _generar_con_ideogram(prompt, creatividad.tipo),
        "gemini":   lambda: _generar_con_gemini(prompt, creatividad.tipo),
    }

    try:
        url_imagen = fn_map[proveedor]()
        extension = "jpg" if any(x in url_imagen.lower() for x in ("jpeg", ".jpg")) else "png"
        ruta_abs, ruta_relativa = _ruta_guardado(creatividad.pk, extension)
        _descargar(url_imagen, ruta_abs)
        return {"ok": True, "ruta": ruta_relativa, "proveedor": proveedor, "interno": False}

    except NotImplementedError as exc:
        return {"ok": False, "error": str(exc), "es_premium": True}
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "es_premium": True}
    except Exception as exc:
        # Detectar errores de saldo/cuenta → mensaje premium amigable
        msg = str(exc).lower()
        if any(x in msg for x in ("balance", "exhausted", "locked", "billing", "quota", "insufficient")):
            return {
                "ok": False,
                "error": _MSG_PREMIUM,
                "es_premium": True,
            }
        return {"ok": False, "error": str(exc), "es_premium": True}


def generar_imagen_fal(creatividad) -> dict:
    """Shortcut para usar Fal AI directamente."""
    return generar_imagen_para_creatividad(creatividad, proveedor="fal")
