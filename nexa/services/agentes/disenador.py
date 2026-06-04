"""
Agente Diseñador — Nexa AI
Genera especificaciones visuales para cada pieza de contenido.

# === PUNTO DE CONEXIÓN API ===
# Reemplazar `generar_brief_visual` con llamada a API de generación de imágenes
# o instrucciones para Canva/Adobe Express cuando se active.
# === FIN PUNTO DE CONEXIÓN ===
"""


def generar_brief_visual(empresa, tipo_contenido: str, titulo: str) -> dict:
    """
    Genera brief visual para una pieza de contenido.
    Retorna dict con: paleta, tipografia, layout, instrucciones.
    """
    return _generar_simulado(empresa, tipo_contenido, titulo)


def _generar_simulado(empresa, tipo_contenido, titulo) -> dict:
    return {
        "paleta": {
            "principal": empresa.color_principal,
            "secundario": empresa.color_secundario,
            "fondo": "#ffffff",
            "texto": "#1a1a2e",
        },
        "tipografia": {
            "titulo": "Inter 700, 28px",
            "cuerpo": "Inter 400, 16px",
            "cta": "Inter 600, 14px",
        },
        "layout": _layout_por_tipo(tipo_contenido),
        "instrucciones": (
            f"Usar colores corporativos de {empresa.nombre_empresa}. "
            f"Mantener identidad visual consistente. "
            f"Logo en esquina superior derecha."
        ),
    }


def _layout_por_tipo(tipo) -> str:
    layouts = {
        "carrusel": "Portada impactante + slides de contenido + slide CTA. Formato cuadrado 1080x1080.",
        "historia": "Vertical 1080x1920. Texto centrado, fondo degradado, sticker interactivo.",
        "post": "Cuadrado 1080x1080. Imagen de fondo + overlay semitransparente + texto.",
        "reel": "Vertical 1080x1920. Subtítulos animados, transición rápida entre escenas.",
        "campana": "Set de piezas coordinadas: post + historia + reel. Paleta unificada.",
    }
    return layouts.get(tipo, "Cuadrado 1080x1080. Diseño limpio y legible.")
