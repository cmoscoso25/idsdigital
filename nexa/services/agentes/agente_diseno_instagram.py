"""
Agente Diseño Instagram — Nexa AI
Genera creatividades visuales profesionales para Instagram.

# === PUNTOS DE CONEXIÓN API ===
# Al activar generación real de imágenes, reemplazar `_generar_imagen_simulada`
# en cada función por la llamada al proveedor correspondiente:
#
# OpenAI Images (DALL-E 3):
#   from openai import OpenAI
#   client = OpenAI()
#   response = client.images.generate(model="dall-e-3", prompt=prompt_visual, size="1024x1024")
#   url = response.data[0].url
#
# Flux (via Replicate):
#   import replicate
#   output = replicate.run("black-forest-labs/flux-schnell", input={"prompt": prompt_visual})
#
# Ideogram:
#   POST https://api.ideogram.ai/generate con {"prompt": prompt_visual}
#
# Gemini Imagen:
#   from google import genai
#   client = genai.Client()
#   response = client.models.generate_images(model="imagen-3.0-generate-002", prompt=prompt_visual)
#
# === FIN PUNTOS DE CONEXIÓN ===
"""


def generar_creatividad(empresa, memoria_marca, contenido) -> dict:
    """
    Genera prompt visual y estructura para una creatividad de Instagram.
    Retorna dict con: prompt_visual, estructura_visual_json.
    """
    tipo = contenido.tipo_contenido
    generadores = {
        "post":     _creatividad_post,
        "historia": _creatividad_historia,
        "carrusel": _creatividad_carrusel,
        "reel":     _creatividad_reel,
        "campana":  _creatividad_post,
    }
    fn = generadores.get(tipo, _creatividad_post)
    return fn(empresa, memoria_marca, contenido)


# ── POST ──────────────────────────────────────────────────────────────────────

def _creatividad_post(empresa, memoria_marca, contenido) -> dict:
    nombre   = empresa.nombre_empresa
    color_p  = empresa.color_principal
    color_s  = empresa.color_secundario
    titulo   = contenido.titulo[:80]
    copy_short = contenido.copy.split("\n")[0][:100]
    cta      = contenido.cta or "Contáctanos →"
    hashtags = contenido.hashtags[:80]
    propuesta = (memoria_marca.propuesta_valor[:80] if memoria_marca
                 else empresa.descripcion[:80])

    prompt_visual = (
        f"Professional Instagram square post (1080x1080px) for {nombre}, "
        f"a {empresa.rubro} company. "
        f"Primary brand color {color_p}, accent {color_s}. "
        f"Clean modern layout with gradient background from {color_p} to {color_s}. "
        f"Bold white headline: '{copy_short}'. "
        f"Subtle brand tagline: '{propuesta}'. "
        f"CTA button: '{cta}'. "
        f"Company logo top-right corner. "
        f"Minimalist design, premium B2B aesthetic, no stock photos."
    )

    estructura = {
        "tipo": "post",
        "dimensiones": "1080×1080",
        "ratio": "1:1",
        "capas": [
            {"orden": 1, "tipo": "fondo_gradiente",
             "color_inicio": color_p, "color_fin": color_s, "angulo": 135},
            {"orden": 2, "tipo": "overlay_oscuro", "opacidad": 0.35},
            {"orden": 3, "tipo": "logo",
             "posicion": "esquina_superior_derecha", "tamanio": "80px"},
            {"orden": 4, "tipo": "titulo",
             "texto": titulo, "fuente": "Inter 700", "tamanio": "36px",
             "color": "#ffffff", "alineacion": "izquierda"},
            {"orden": 5, "tipo": "subtitulo",
             "texto": copy_short, "fuente": "Inter 400", "tamanio": "18px",
             "color": "rgba(255,255,255,0.85)"},
            {"orden": 6, "tipo": "cta_boton",
             "texto": cta, "color_fondo": "#ffffff",
             "color_texto": color_p, "posicion": "inferior"},
            {"orden": 7, "tipo": "hashtags",
             "texto": hashtags[:50], "tamanio": "12px",
             "color": "rgba(255,255,255,0.5)"},
        ],
        "colores": {"principal": color_p, "secundario": color_s,
                    "texto": "#ffffff", "cta_fondo": "#ffffff"},
        "tipografia": "Inter",
        "logo_empresa": bool(empresa.logo),
    }

    return {"prompt_visual": prompt_visual, "estructura_visual_json": estructura}


# ── HISTORIA ──────────────────────────────────────────────────────────────────

def _creatividad_historia(empresa, memoria_marca, contenido) -> dict:
    nombre  = empresa.nombre_empresa
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    cta     = contenido.cta or "Ver más → Link en bio"
    copy_lines = [l.strip() for l in contenido.copy.split("\n") if l.strip()]

    pantallas_contenido = contenido.estructura_json.get("pantallas", [])

    prompt_visual = (
        f"Professional Instagram Story series (1080x1920px) for {nombre}. "
        f"3 vertically-designed screens. "
        f"Screen 1: bold question or hook — '{copy_lines[0] if copy_lines else contenido.titulo}', "
        f"gradient {color_p} to {color_s}, interactive poll sticker. "
        f"Screen 2: brand proposition — '{(memoria_marca.propuesta_valor[:80] if memoria_marca else '')}', "
        f"dark background #{_hex_dark(color_p)}, swipe-up animation. "
        f"Screen 3: CTA — '{cta}', link sticker. "
        f"Clean typography, brand logo on each screen, premium quality."
    )

    pantallas = []
    for i, p in enumerate(pantallas_contenido[:3], 1):
        pantallas.append({
            "numero": i,
            "titulo": p.get("texto", ""),
            "subtitulo": p.get("subtexto", ""),
            "color_fondo": color_p if i == 1 else (color_s if i == 2 else "#0f172a"),
            "sticker": p.get("sticker", "link"),
            "duracion": p.get("duracion", "7s"),
        })

    if not pantallas:
        pantallas = [
            {"numero": 1, "titulo": contenido.titulo[:60], "subtitulo": "",
             "color_fondo": color_p, "sticker": "encuesta", "duracion": "7s"},
            {"numero": 2, "titulo": copy_lines[0][:80] if copy_lines else "",
             "subtitulo": nombre, "color_fondo": color_s, "sticker": "deslizador", "duracion": "7s"},
            {"numero": 3, "titulo": cta, "subtitulo": "🔗 Link en bio",
             "color_fondo": "#0f172a", "sticker": "link", "duracion": "6s"},
        ]

    estructura = {
        "tipo": "historia",
        "dimensiones": "1080×1920",
        "ratio": "9:16",
        "pantallas": pantallas,
        "colores": {"principal": color_p, "secundario": color_s},
        "tipografia": "Inter",
    }

    return {"prompt_visual": prompt_visual, "estructura_visual_json": estructura}


# ── CARRUSEL ──────────────────────────────────────────────────────────────────

def _creatividad_carrusel(empresa, memoria_marca, contenido) -> dict:
    nombre  = empresa.nombre_empresa
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    cta     = contenido.cta or "Contáctanos →"

    diapositivas = contenido.estructura_json.get("diapositivas", [])

    prompt_visual = (
        f"Professional Instagram Carousel (1080x1080px each) for {nombre}. "
        f"{len(diapositivas) or 5} slides. "
        f"Slide 1 (Cover): bold hook — '{contenido.titulo[:60]}', gradient {color_p} to {color_s}. "
        f"Slides 2-4: clean content layout, dark background #0f172a, brand accent {color_p}. "
        f"Final slide (CTA): '{cta}', gradient background, logo centered. "
        f"Consistent typography Inter, brand colors throughout, premium B2B look."
    )

    slides = []
    tipo_color = {
        "portada":   color_p,
        "problema":  "#1e293b",
        "contenido": "#1e293b",
        "beneficio": "#162032",
        "cierre":    "#162032",
        "cta":       color_s,
    }

    for d in diapositivas:
        slides.append({
            "numero":      d.get("numero", 1),
            "tipo":        d.get("tipo", "contenido"),
            "titulo":      d.get("texto", ""),
            "subtitulo":   d.get("subtexto", ""),
            "color_fondo": tipo_color.get(d.get("tipo", "contenido"), "#1e293b"),
            "color_acento": color_p,
        })

    if not slides:
        slides = [
            {"numero": 1, "tipo": "portada",   "titulo": contenido.titulo[:60],
             "subtitulo": f"Por {nombre}", "color_fondo": color_p, "color_acento": "#ffffff"},
            {"numero": 2, "tipo": "problema",  "titulo": "¿Cuál es el problema?",
             "subtitulo": "", "color_fondo": "#1e293b", "color_acento": color_p},
            {"numero": 3, "tipo": "contenido", "titulo": "La solución existe",
             "subtitulo": "", "color_fondo": "#1e293b", "color_acento": color_p},
            {"numero": 4, "tipo": "beneficio", "titulo": "El beneficio para ti",
             "subtitulo": "", "color_fondo": "#162032", "color_acento": color_s},
            {"numero": 5, "tipo": "cta",       "titulo": cta,
             "subtitulo": nombre, "color_fondo": color_s, "color_acento": "#ffffff"},
        ]

    estructura = {
        "tipo": "carrusel",
        "dimensiones": "1080×1080",
        "ratio": "1:1",
        "total_slides": len(slides),
        "slides": slides,
        "colores": {"principal": color_p, "secundario": color_s},
        "tipografia": "Inter",
    }

    return {"prompt_visual": prompt_visual, "estructura_visual_json": estructura}


# ── REEL ──────────────────────────────────────────────────────────────────────

def _creatividad_reel(empresa, memoria_marca, contenido) -> dict:
    nombre  = empresa.nombre_empresa
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    cta     = contenido.cta or "Síguenos para más"

    escenas_contenido = contenido.estructura_json.get("escenas", [])
    hook = contenido.estructura_json.get("hook", contenido.titulo[:60])

    prompt_visual = (
        f"Professional Instagram Reel storyboard (1080x1920px, 30s) for {nombre}. "
        f"4 scenes. "
        f"Scene 1 (Hook, 0-5s): '{hook}', bold text animation on gradient {color_p}. "
        f"Scene 2 (Development, 5-15s): brand message, dark background, subtitle animation. "
        f"Scene 3 (Example, 15-25s): visual demonstration, brand colors. "
        f"Scene 4 (CTA, 25-30s): '{cta}', logo + call to action. "
        f"Fast cuts, text-on-screen style, premium motion graphics."
    )

    escenas = []
    tipo_color = {
        "hook":       color_p,
        "desarrollo": "#1e293b",
        "ejemplo":    "#162032",
        "cta":        color_s,
    }

    for e in escenas_contenido:
        escenas.append({
            "numero":      escenas_contenido.index(e) + 1,
            "tipo":        e.get("tipo", "desarrollo"),
            "texto":       e.get("texto", ""),
            "rango":       e.get("rango", ""),
            "color_fondo": tipo_color.get(e.get("tipo", "desarrollo"), "#1e293b"),
            "transicion":  "corte" if e.get("tipo") == "hook" else "fundido",
        })

    if not escenas:
        escenas = [
            {"numero": 1, "tipo": "hook",       "texto": hook,
             "rango": "0-5s",   "color_fondo": color_p, "transicion": "corte"},
            {"numero": 2, "tipo": "desarrollo", "texto": contenido.copy.split("\n")[0][:80],
             "rango": "5-15s",  "color_fondo": "#1e293b", "transicion": "fundido"},
            {"numero": 3, "tipo": "ejemplo",    "texto": f"Con {nombre} lo logramos",
             "rango": "15-25s", "color_fondo": "#162032", "transicion": "corte"},
            {"numero": 4, "tipo": "cta",        "texto": cta,
             "rango": "25-30s", "color_fondo": color_s, "transicion": "fundido"},
        ]

    estructura = {
        "tipo": "reel",
        "dimensiones": "1080×1920",
        "ratio": "9:16",
        "duracion_total": "30s",
        "hook": hook,
        "escenas": escenas,
        "colores": {"principal": color_p, "secundario": color_s},
        "tipografia": "Inter",
    }

    return {"prompt_visual": prompt_visual, "estructura_visual_json": estructura}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hex_dark(hex_color: str) -> str:
    """Versión oscura de un color hex para fondos."""
    return "0f172a"
