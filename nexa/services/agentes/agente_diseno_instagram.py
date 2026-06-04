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
    Genera prompt visual, estructura y render HTML para una creatividad Instagram.
    Retorna dict con: prompt_visual, estructura_visual_json, render_html, render_css.
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

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_post(empresa, contenido, estructura),
        "render_css": "",
    }


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

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_historia(empresa, contenido, estructura),
        "render_css": "",
    }


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

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_carrusel(empresa, contenido, estructura),
        "render_css": "",
    }


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

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_reel(empresa, contenido, estructura),
        "render_css": "",
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hex_dark(hex_color: str) -> str:
    """Versión oscura de un color hex para fondos."""
    return "0f172a"


# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE RENDER HTML — server-side Instagram mockups
# Genera HTML inline-styled auto-contenido.
# Para reemplazar por imagen real: cambiar solo la función _render_* correspondiente
# y devolver <img src="url_de_api"> en su lugar.
# ══════════════════════════════════════════════════════════════════════════════

def _s(text, maxlen=80):
    """Trunca y escapa texto para HTML."""
    return str(text or "")[:maxlen].replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── Detección de categoría visual ─────────────────────────────────────────────

def _detectar_categoria(contenido, empresa) -> str:
    texto = (
        f"{contenido.titulo} {contenido.copy[:300]} {empresa.rubro} "
        f"{empresa.descripcion[:100]}"
    ).lower()

    if any(w in texto for w in ["ia ", " ia", "inteligencia artificial", "neural", "machine learning", "llm", "gpt", "agente ia"]):
        return "ia"
    if any(w in texto for w in ["automati", "rpa", "flujo", "proceso automati", "robot", "workflow"]):
        return "automatizacion"
    if any(w in texto for w in ["software", "código", "desarrollo", "programaci", "app ", "sistema", "dashboard", "erp", "crm"]):
        return "software"
    if any(w in texto for w in ["marketing", "publicidad", "campaña", "brand", "lead", "conversion", "contenido", "estrategia"]):
        return "marketing"
    if any(w in texto for w in ["educat", "aprend", "curso", "formaci", "capacit", "conocimiento", "aprendizaje"]):
        return "educacion"
    if any(w in texto for w in ["finanz", "dinero", "inversion", "contabilidad", "presupuesto", "revenue", "factura"]):
        return "finanzas"
    if any(w in texto for w in ["productiv", "eficienci", "optimiz", "ahorro tiempo", "rendimiento", "flujo trabajo"]):
        return "productividad"
    if any(w in texto for w in ["transform", "digital", "innovaci", "futuro", "disrupci"]):
        return "transformacion"
    if any(w in texto for w in ["salud", "médic", "clínic", "bienestar", "hospital"]):
        return "salud"
    return "tecnologia"


# ── Biblioteca visual por categoría ───────────────────────────────────────────

def _bloque_visual(categoria: str, c1: str, c2: str) -> dict:
    """
    Retorna los elementos visuales SVG para una categoría.
    hero: SVG grande para área central del post
    pattern: patrón de fondo sutil
    icon: emoji / unicode del sector
    kpi_cards: HTML de cards métricas (para carrusel beneficio/cta)
    slide_visuals: dict de SVGs por tipo de slide
    """
    b = _BLOQUES[categoria] if categoria in _BLOQUES else _BLOQUES["tecnologia"]
    return b(c1, c2)


def _blq_ia(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:0;right:0;width:55%;height:55%;opacity:0.18">
  <defs>
    <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g stroke="white" stroke-width="0.6" fill="none" opacity="0.7">
    <line x1="40" y1="60" x2="100" y2="40"/><line x1="40" y1="60" x2="100" y2="80"/><line x1="40" y1="60" x2="100" y2="120"/>
    <line x1="40" y1="120" x2="100" y2="80"/><line x1="40" y1="120" x2="100" y2="120"/><line x1="40" y1="120" x2="100" y2="160"/>
    <line x1="40" y1="180" x2="100" y2="120"/><line x1="40" y1="180" x2="100" y2="160"/><line x1="40" y1="180" x2="100" y2="200"/>
    <line x1="100" y1="40" x2="160" y2="60"/><line x1="100" y1="40" x2="160" y2="100"/>
    <line x1="100" y1="80" x2="160" y2="60"/><line x1="100" y1="80" x2="160" y2="100"/><line x1="100" y1="80" x2="160" y2="140"/>
    <line x1="100" y1="120" x2="160" y2="100"/><line x1="100" y1="120" x2="160" y2="140"/><line x1="100" y1="120" x2="160" y2="180"/>
    <line x1="100" y1="160" x2="160" y2="140"/><line x1="100" y1="160" x2="160" y2="180"/>
    <line x1="100" y1="200" x2="160" y2="180"/>
    <line x1="160" y1="60" x2="210" y2="80"/><line x1="160" y1="100" x2="210" y2="80"/><line x1="160" y1="100" x2="210" y2="130"/>
    <line x1="160" y1="140" x2="210" y2="130"/><line x1="160" y1="180" x2="210" y2="130"/>
  </g>
  <g filter="url(#glow)">
    <circle cx="40" cy="60" r="5" fill="white" opacity="0.9"/><circle cx="40" cy="120" r="5" fill="white" opacity="0.9"/><circle cx="40" cy="180" r="5" fill="white" opacity="0.9"/>
    <circle cx="100" cy="40" r="6" fill="{c1}" opacity="1"/><circle cx="100" cy="80" r="6" fill="{c1}"/><circle cx="100" cy="120" r="7" fill="white"/><circle cx="100" cy="160" r="6" fill="{c1}"/><circle cx="100" cy="200" r="5" fill="{c1}" opacity="0.8"/>
    <circle cx="160" cy="60" r="5" fill="white" opacity="0.8"/><circle cx="160" cy="100" r="5" fill="white" opacity="0.8"/><circle cx="160" cy="140" r="5" fill="white" opacity="0.8"/><circle cx="160" cy="180" r="5" fill="white" opacity="0.8"/>
    <circle cx="210" cy="80" r="5" fill="white" opacity="0.7"/><circle cx="210" cy="130" r="5" fill="white" opacity="0.7"/>
  </g>
</svg>"""
    chip = f"""<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" style="width:56px;height:56px;opacity:0.85">
  <rect x="20" y="20" width="40" height="40" rx="6" fill="none" stroke="white" stroke-width="1.5"/>
  <rect x="28" y="28" width="24" height="24" rx="3" fill="white" fill-opacity="0.15"/>
  <g stroke="white" stroke-width="1.2" opacity="0.7">
    <line x1="30" y1="20" x2="30" y2="12"/><line x1="40" y1="20" x2="40" y2="12"/><line x1="50" y1="20" x2="50" y2="12"/>
    <line x1="30" y1="60" x2="30" y2="68"/><line x1="40" y1="60" x2="40" y2="68"/><line x1="50" y1="60" x2="50" y2="68"/>
    <line x1="20" y1="30" x2="12" y2="30"/><line x1="20" y1="40" x2="12" y2="40"/><line x1="20" y1="50" x2="12" y2="50"/>
    <line x1="60" y1="30" x2="68" y2="30"/><line x1="60" y1="40" x2="68" y2="40"/><line x1="60" y1="50" x2="68" y2="50"/>
  </g>
  <text x="40" y="44" text-anchor="middle" font-size="11" fill="white" font-family="monospace" font-weight="700">AI</text>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "⬡", "label": "INTELIGENCIA ARTIFICIAL",
            "pattern": _pattern_dots(), "slide_accent": _slide_accent_ia(c1)}


def _blq_automatizacion(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:-10px;right:-10px;width:50%;height:50%;opacity:0.2">
  <g fill="none" stroke="white" stroke-width="1">
    <!-- Gear 1 -->
    <circle cx="70" cy="80" r="28" stroke-width="1.5" opacity="0.8"/>
    <circle cx="70" cy="80" r="18" fill="white" fill-opacity="0.08"/>
    <circle cx="70" cy="80" r="6" fill="white" fill-opacity="0.4"/>
    <g transform="rotate(0 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(45 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(90 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(135 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(180 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(225 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(270 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <g transform="rotate(315 70 80)"><rect x="66" y="48" width="8" height="10" rx="2" fill="white" fill-opacity="0.5"/></g>
    <!-- Gear 2 smaller -->
    <circle cx="120" cy="110" r="18" stroke-width="1.2" opacity="0.6"/>
    <circle cx="120" cy="110" r="11" fill="white" fill-opacity="0.05"/>
    <circle cx="120" cy="110" r="4" fill="white" fill-opacity="0.3"/>
    <g transform="rotate(22 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <g transform="rotate(82 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <g transform="rotate(142 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <g transform="rotate(202 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <g transform="rotate(262 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <g transform="rotate(322 120 110)"><rect x="117" y="89" width="6" height="8" rx="1.5" fill="white" fill-opacity="0.4"/></g>
    <!-- Flow arrows -->
    <path d="M30 150 L80 150 L80 165 L110 155 L80 145 L80 150" fill="white" fill-opacity="0.25" stroke="none"/>
    <path d="M30 170 Q 80 170 130 155" stroke-dasharray="4,3" opacity="0.4"/>
  </g>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <circle cx="30" cy="30" r="20" fill="none" stroke="white" stroke-width="1.5" opacity="0.8"/>
  <circle cx="30" cy="30" r="12" fill="white" fill-opacity="0.1"/>
  <g transform="rotate(0 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <g transform="rotate(60 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <g transform="rotate(120 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <g transform="rotate(180 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <g transform="rotate(240 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <g transform="rotate(300 30 30)"><rect x="27" y="6" width="6" height="8" rx="1.5" fill="white" opacity="0.6"/></g>
  <circle cx="30" cy="30" r="5" fill="white" opacity="0.7"/>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "⚙", "label": "AUTOMATIZACIÓN",
            "pattern": _pattern_grid(), "slide_accent": _slide_accent_flow(c1)}


def _blq_software(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 220 180" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:8px;right:8px;width:52%;height:44%;opacity:0.22">
  <!-- Laptop screen -->
  <rect x="20" y="10" width="160" height="110" rx="6" fill="none" stroke="white" stroke-width="1.5"/>
  <rect x="25" y="15" width="150" height="100" rx="3" fill="white" fill-opacity="0.06"/>
  <!-- Screen content: dashboard bars -->
  <rect x="32" y="22" width="60" height="10" rx="2" fill="white" fill-opacity="0.2"/>
  <rect x="100" y="22" width="40" height="10" rx="2" fill="white" fill-opacity="0.15"/>
  <rect x="148" y="22" width="22" height="10" rx="2" fill="white" fill-opacity="0.1"/>
  <!-- KPI cards -->
  <rect x="32" y="38" width="42" height="28" rx="3" fill="white" fill-opacity="0.1" stroke="white" stroke-width="0.5" stroke-opacity="0.3"/>
  <rect x="80" y="38" width="42" height="28" rx="3" fill="{c1}" fill-opacity="0.25" stroke="white" stroke-width="0.5" stroke-opacity="0.3"/>
  <rect x="128" y="38" width="42" height="28" rx="3" fill="white" fill-opacity="0.1" stroke="white" stroke-width="0.5" stroke-opacity="0.3"/>
  <!-- Bars -->
  <g fill="white">
    <rect x="38" y="72" width="8" height="30" rx="2" opacity="0.3"/>
    <rect x="52" y="62" width="8" height="40" rx="2" opacity="0.5"/>
    <rect x="66" y="78" width="8" height="24" rx="2" opacity="0.3"/>
    <rect x="80" y="55" width="8" height="47" rx="2" opacity="0.7"/>
    <rect x="94" y="68" width="8" height="34" rx="2" opacity="0.5"/>
    <rect x="108" y="72" width="8" height="30" rx="2" opacity="0.4"/>
    <rect x="122" y="58" width="8" height="44" rx="2" opacity="0.6"/>
    <rect x="136" y="74" width="8" height="28" rx="2" opacity="0.3"/>
    <rect x="150" y="65" width="8" height="37" rx="2" opacity="0.5"/>
    <rect x="164" y="70" width="8" height="32" rx="2" opacity="0.4"/>
  </g>
  <!-- Trend line -->
  <polyline points="42,95 56,82 70,90 84,72 98,79 112,82 126,68 140,74 154,70 168,62" fill="none" stroke="{c1}" stroke-width="1.5" opacity="0.8"/>
  <!-- Base laptop -->
  <path d="M10 122 L190 122 L195 130 L5 130 Z" fill="white" fill-opacity="0.08" stroke="white" stroke-width="0.8" stroke-opacity="0.3"/>
  <rect x="80" y="130" width="40" height="4" rx="2" fill="white" fill-opacity="0.15"/>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <rect x="8" y="10" width="44" height="34" rx="4" fill="none" stroke="white" stroke-width="1.5" opacity="0.8"/>
  <rect x="12" y="14" width="36" height="26" rx="2" fill="white" fill-opacity="0.1"/>
  <g fill="white" opacity="0.6">
    <rect x="15" y="17" width="12" height="4" rx="1"/><rect x="30" y="17" width="14" height="4" rx="1" opacity="0.4"/>
    <rect x="15" y="24" width="5" height="10" rx="1"/><rect x="22" y="27" width="5" height="7" rx="1"/><rect x="29" y="22" width="5" height="12" rx="1"/>
    <rect x="36" y="25" width="5" height="9" rx="1" opacity="0.5"/>
  </g>
  <path d="M22 50 L28 50 L28 44 L32 44 L32 50 L38 50" stroke="white" stroke-width="1.2" fill="none" opacity="0.5"/>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "◧", "label": "SOFTWARE",
            "pattern": _pattern_grid(), "slide_accent": _slide_accent_dashboard(c1)}


def _blq_marketing(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:0;right:0;width:54%;height:54%;opacity:0.2">
  <!-- Chart bars -->
  <g fill="white">
    <rect x="20" y="120" width="22" height="60" rx="3" opacity="0.3"/>
    <rect x="50" y="95" width="22" height="85" rx="3" opacity="0.4"/>
    <rect x="80" y="75" width="22" height="105" rx="3" opacity="0.5"/>
    <rect x="110" y="50" width="22" height="130" rx="3" opacity="0.7"/>
    <rect x="140" y="30" width="22" height="150" rx="3" opacity="0.9"/>
  </g>
  <!-- Growth arrow -->
  <path d="M15 145 Q 55 130 85 110 T 155 40" fill="none" stroke="white" stroke-width="2" stroke-dasharray="6,3" opacity="0.6"/>
  <polygon points="155,30 165,50 145,50" fill="white" opacity="0.6"/>
  <!-- X-axis -->
  <line x1="10" y1="185" x2="180" y2="185" stroke="white" stroke-width="0.8" opacity="0.3"/>
  <!-- Growth % badge -->
  <rect x="148" y="8" width="46" height="22" rx="11" fill="white" fill-opacity="0.15"/>
  <text x="171" y="23" text-anchor="middle" font-size="11" fill="white" font-weight="700" font-family="sans-serif">+48%</text>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <g fill="white">
    <rect x="8" y="34" width="8" height="18" rx="2" opacity="0.5"/>
    <rect x="20" y="26" width="8" height="26" rx="2" opacity="0.7"/>
    <rect x="32" y="18" width="8" height="34" rx="2" opacity="0.9"/>
    <rect x="44" y="10" width="8" height="42" rx="2"/>
  </g>
  <path d="M12 36 Q 25 28 36 20 L 48 12" fill="none" stroke="white" stroke-width="1.8" opacity="0.8"/>
  <polygon points="48,8 55,18 41,18" fill="white" opacity="0.8"/>
  <line x1="6" y1="54" x2="54" y2="54" stroke="white" stroke-width="1" opacity="0.4"/>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "◈", "label": "MARKETING DIGITAL",
            "pattern": _pattern_dots(), "slide_accent": _slide_accent_chart(c1)}


def _blq_productividad(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:5px;right:5px;width:50%;height:50%;opacity:0.2">
  <!-- Progress ring -->
  <circle cx="100" cy="100" r="70" fill="none" stroke="white" stroke-width="2" opacity="0.15"/>
  <circle cx="100" cy="100" r="70" fill="none" stroke="white" stroke-width="4" stroke-dasharray="307 440" stroke-dashoffset="-55" stroke-linecap="round" opacity="0.9"/>
  <circle cx="100" cy="100" r="52" fill="none" stroke="white" stroke-width="2.5" stroke-dasharray="220 327" stroke-dashoffset="-40" stroke-linecap="round" opacity="0.6"/>
  <circle cx="100" cy="100" r="34" fill="none" stroke="white" stroke-width="2" stroke-dasharray="170 213" stroke-dashoffset="-30" stroke-linecap="round" opacity="0.4"/>
  <!-- Tasks -->
  <g fill="none" stroke="white" stroke-width="1.2" opacity="0.7">
    <rect x="118" y="40" width="55" height="10" rx="2"/>
    <rect x="118" y="56" width="40" height="10" rx="2"/>
    <rect x="118" y="72" width="50" height="10" rx="2"/>
  </g>
  <g fill="white" opacity="0.7">
    <circle cx="113" cy="45" r="4"/><text x="113" y="49" text-anchor="middle" font-size="5" fill="black">✓</text>
    <circle cx="113" cy="61" r="4"/><text x="113" y="65" text-anchor="middle" font-size="5" fill="black">✓</text>
    <circle cx="113" cy="77" r="4" fill="none" stroke="white" stroke-width="1"/>
  </g>
  <!-- Center % -->
  <text x="100" y="107" text-anchor="middle" font-size="20" fill="white" font-weight="800" font-family="sans-serif">70%</text>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <circle cx="30" cy="30" r="24" fill="none" stroke="white" stroke-width="2" opacity="0.3"/>
  <circle cx="30" cy="30" r="24" fill="none" stroke="white" stroke-width="3" stroke-dasharray="105 150" stroke-dashoffset="-18" stroke-linecap="round"/>
  <text x="30" y="35" text-anchor="middle" font-size="13" fill="white" font-weight="800" font-family="sans-serif">70%</text>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "◎", "label": "PRODUCTIVIDAD",
            "pattern": _pattern_grid(), "slide_accent": _slide_accent_progress(c1)}


def _blq_transformacion(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:0;right:0;width:52%;height:52%;opacity:0.18">
  <defs><filter id="glt"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <!-- Hexagons -->
  <g fill="white" stroke="none">
    <polygon points="100,20 120,32 120,56 100,68 80,56 80,32" opacity="0.12"/>
    <polygon points="100,20 120,32 120,56 100,68 80,56 80,32" fill="none" stroke="white" stroke-width="1.2" opacity="0.6"/>
    <polygon points="130,68 150,80 150,104 130,116 110,104 110,80" opacity="0.08"/>
    <polygon points="130,68 150,80 150,104 130,116 110,104 110,80" fill="none" stroke="white" stroke-width="0.8" opacity="0.4"/>
    <polygon points="70,68 90,80 90,104 70,116 50,104 50,80" opacity="0.08"/>
    <polygon points="70,68 90,80 90,104 70,116 50,104 50,80" fill="none" stroke="white" stroke-width="0.8" opacity="0.4"/>
    <polygon points="100,116 120,128 120,152 100,164 80,152 80,128" opacity="0.1"/>
    <polygon points="100,116 120,128 120,152 100,164 80,152 80,128" fill="none" stroke="white" stroke-width="1" opacity="0.5"/>
  </g>
  <g filter="url(#glt)">
    <circle cx="100" cy="44" r="6" fill="white" opacity="0.9"/>
    <circle cx="130" cy="92" r="5" fill="{c1}" opacity="0.9"/>
    <circle cx="70" cy="92" r="5" fill="{c1}" opacity="0.9"/>
    <circle cx="100" cy="140" r="6" fill="white" opacity="0.9"/>
  </g>
  <g stroke="white" stroke-width="0.8" opacity="0.4">
    <line x1="100" y1="68" x2="110" y2="80"/><line x1="100" y1="68" x2="90" y2="80"/>
    <line x1="110" y1="104" x2="100" y2="116"/><line x1="90" y1="104" x2="100" y2="116"/>
  </g>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <polygon points="30,6 44,14 44,30 30,38 16,30 16,14" fill="none" stroke="white" stroke-width="1.5" opacity="0.9"/>
  <polygon points="30,14 38,19 38,29 30,34 22,29 22,19" fill="white" fill-opacity="0.15"/>
  <circle cx="30" cy="24" r="5" fill="white" opacity="0.9"/>
  <path d="M20 46 L30 38 L40 46" stroke="white" stroke-width="1.2" fill="none" opacity="0.6"/>
  <path d="M24 54 L30 46 L36 54" stroke="white" stroke-width="1" fill="none" opacity="0.4"/>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "⬡", "label": "TRANSFORMACIÓN DIGITAL",
            "pattern": _pattern_dots(), "slide_accent": _slide_accent_ia(c1)}


def _blq_tecnologia(c1, c2):
    svg_hero = f"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="position:absolute;top:0;right:0;width:52%;height:52%;opacity:0.18">
  <!-- Circuit board -->
  <g stroke="white" stroke-width="0.8" fill="none" opacity="0.6">
    <line x1="30" y1="50" x2="80" y2="50"/><line x1="80" y1="50" x2="80" y2="80"/><line x1="80" y1="80" x2="130" y2="80"/>
    <line x1="50" y1="80" x2="50" y2="120"/><line x1="50" y1="120" x2="100" y2="120"/>
    <line x1="100" y1="50" x2="100" y2="80"/><line x1="100" y1="80" x2="150" y2="80"/><line x1="150" y1="80" x2="150" y2="130"/>
    <line x1="130" y1="80" x2="130" y2="140"/><line x1="100" y1="140" x2="160" y2="140"/>
    <line x1="60" y1="140" x2="80" y2="140"/><line x1="80" y1="120" x2="80" y2="160"/>
  </g>
  <g fill="white">
    <rect x="76" y="46" width="8" height="8" rx="1" opacity="0.6"/>
    <rect x="96" y="76" width="8" height="8" rx="1" opacity="0.6"/>
    <rect x="126" y="76" width="8" height="8" rx="1" opacity="0.8"/>
    <rect x="46" y="116" width="8" height="8" rx="1" opacity="0.5"/>
    <rect x="96" y="116" width="8" height="8" rx="1" opacity="0.7"/>
    <rect x="146" y="76" width="8" height="8" rx="1" opacity="0.6"/>
    <rect x="146" y="126" width="8" height="8" rx="1" opacity="0.5"/>
    <rect x="76" y="156" width="8" height="8" rx="1" opacity="0.5"/>
    <circle cx="50" cy="50" r="5" opacity="0.8"/>
    <circle cx="130" cy="140" r="5" opacity="0.8"/>
  </g>
</svg>"""
    chip = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" style="width:52px;height:52px;opacity:0.9">
  <g stroke="white" stroke-width="1.2" fill="none" opacity="0.7">
    <line x1="10" y1="20" x2="30" y2="20"/><line x1="30" y1="20" x2="30" y2="30"/><line x1="30" y1="30" x2="50" y2="30"/>
    <line x1="20" y1="30" x2="20" y2="40"/><line x1="20" y1="40" x2="40" y2="40"/><line x1="40" y1="30" x2="40" y2="50"/>
  </g>
  <g fill="white" opacity="0.8">
    <rect x="26" y="16" width="8" height="8" rx="1.5"/><rect x="36" y="26" width="8" height="8" rx="1.5"/>
    <rect x="16" y="36" width="8" height="8" rx="1.5"/><rect x="36" y="46" width="8" height="8" rx="1.5"/>
    <circle cx="10" cy="20" r="3"/><circle cx="50" cy="30" r="3"/>
  </g>
</svg>"""
    return {"hero": svg_hero, "chip": chip, "icon": "◈", "label": "TECNOLOGÍA",
            "pattern": _pattern_grid(), "slide_accent": _slide_accent_ia(c1)}


# Educación, Finanzas, Salud — variantes del patrón base
def _blq_educacion(c1, c2):
    b = _blq_productividad(c1, c2)
    b.update({"label": "EDUCACIÓN", "icon": "◉"})
    return b

def _blq_finanzas(c1, c2):
    b = _blq_marketing(c1, c2)
    b.update({"label": "FINANZAS", "icon": "◇"})
    return b

def _blq_salud(c1, c2):
    b = _blq_transformacion(c1, c2)
    b.update({"label": "SALUD & BIENESTAR", "icon": "◍"})
    return b


_BLOQUES = {
    "ia": _blq_ia,
    "automatizacion": _blq_automatizacion,
    "software": _blq_software,
    "marketing": _blq_marketing,
    "productividad": _blq_productividad,
    "transformacion": _blq_transformacion,
    "educacion": _blq_educacion,
    "finanzas": _blq_finanzas,
    "salud": _blq_salud,
    "tecnologia": _blq_tecnologia,
}


# ── Patrones de fondo SVG ──────────────────────────────────────────────────────

def _pattern_dots() -> str:
    return """<svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.07" xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="pd" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.5" fill="white"/>
  </pattern></defs>
  <rect width="100%" height="100%" fill="url(#pd)"/>
</svg>"""

def _pattern_grid() -> str:
    return """<svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.06" xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="pg" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0 L0 0 0 32" fill="none" stroke="white" stroke-width="0.5"/>
  </pattern></defs>
  <rect width="100%" height="100%" fill="url(#pg)"/>
</svg>"""


# ── Accentos por tipo de slide ─────────────────────────────────────────────────

def _slide_accent_ia(c1) -> dict:
    return {
        "portada":   f'<div style="font-size:48px;opacity:0.15;position:absolute;bottom:16px;right:16px;line-height:1">⬡⬡</div>',
        "problema":  f'<div style="font-size:36px;opacity:0.15;position:absolute;top:16px;right:16px">⁇</div>',
        "contenido": f'<div style="opacity:0.12;position:absolute;bottom:8px;right:8px;font-size:32px">◈◈◈</div>',
        "beneficio": f'<div style="color:{c1};opacity:0.25;position:absolute;top:12px;right:12px;font-size:40px">✓</div>',
        "cta":       f'<div style="font-size:44px;opacity:0.12;position:absolute;bottom:12px;right:12px">★</div>',
    }

def _slide_accent_flow(c1) -> dict:
    return {
        "portada":   f'<div style="font-size:48px;opacity:0.15;position:absolute;bottom:12px;right:12px">⚙⚙</div>',
        "problema":  f'<div style="font-size:40px;opacity:0.15;position:absolute;top:12px;right:12px">→→</div>',
        "contenido": f'<div style="opacity:0.12;position:absolute;bottom:8px;right:8px;font-size:36px">⚙</div>',
        "beneficio": f'<div style="color:{c1};opacity:0.2;position:absolute;top:12px;right:12px;font-size:40px">✓</div>',
        "cta":       f'<div style="font-size:44px;opacity:0.12;position:absolute;bottom:12px;right:12px">▶</div>',
    }

def _slide_accent_dashboard(c1) -> dict:
    return {
        "portada":   f'<div style="font-size:44px;opacity:0.15;position:absolute;bottom:12px;right:12px">◧◧</div>',
        "problema":  f'<div style="font-size:36px;opacity:0.13;position:absolute;top:12px;right:12px">⁇</div>',
        "contenido": f'<div style="opacity:0.12;position:absolute;bottom:8px;right:8px;font-size:32px">▦</div>',
        "beneficio": f'<div style="color:{c1};opacity:0.2;position:absolute;top:12px;right:12px;font-size:40px">↗</div>',
        "cta":       f'<div style="font-size:44px;opacity:0.13;position:absolute;bottom:12px;right:12px">◧</div>',
    }

def _slide_accent_chart(c1) -> dict:
    return {
        "portada":   f'<div style="font-size:44px;opacity:0.13;position:absolute;bottom:12px;right:12px">▲▲</div>',
        "problema":  f'<div style="font-size:40px;opacity:0.13;position:absolute;top:12px;right:12px">↘</div>',
        "contenido": f'<div style="opacity:0.12;position:absolute;bottom:8px;right:8px;font-size:36px">◈</div>',
        "beneficio": f'<div style="color:{c1};opacity:0.2;position:absolute;top:12px;right:12px;font-size:40px">↗</div>',
        "cta":       f'<div style="font-size:44px;opacity:0.12;position:absolute;bottom:12px;right:12px">★</div>',
    }

def _slide_accent_progress(c1) -> dict:
    return {
        "portada":   f'<div style="font-size:44px;opacity:0.13;position:absolute;bottom:12px;right:12px">◎◎</div>',
        "problema":  f'<div style="font-size:40px;opacity:0.14;position:absolute;top:12px;right:12px">⁇</div>',
        "contenido": f'<div style="opacity:0.12;position:absolute;bottom:8px;right:8px;font-size:36px">◎</div>',
        "beneficio": f'<div style="color:{c1};opacity:0.22;position:absolute;top:12px;right:12px;font-size:40px">✓</div>',
        "cta":       f'<div style="font-size:44px;opacity:0.12;position:absolute;bottom:12px;right:12px">▶</div>',
    }


# ── KPI cards por categoría ────────────────────────────────────────────────────

def _kpi_cards(categoria: str, c1: str) -> str:
    metricas = {
        "ia":            [("98.5%", "Precisión IA"), ("73%",  "Tiempo ↓"),  ("4.2x", "ROI")],
        "automatizacion":[("85%",   "Automatizado"), ("10x",  "Velocidad"), ("0%",   "Errores")],
        "software":      [("99.9%", "Uptime"),        ("<1s",  "Carga"),    ("4.8★", "Rating")],
        "marketing":     [("+48%",  "Crecimiento"),   ("3.2%", "CTR"),      ("6.1x", "ROAS")],
        "productividad": [("70%",   "Eficiencia"),    ("8h/w", "Ahorradas"),("3x",   "Output")],
        "transformacion":[("+92%",  "Digital."),      ("-45%", "Costos"),   ("3.8x", "ROI")],
        "educacion":     [("94%",   "Completado"),    ("4.9★", "Satisfac."),("-60%", "Tiempo")],
        "finanzas":      [("+28%",  "ROI"),           ("-42%", "Costos"),   ("+18%", "Ingresos")],
        "salud":         [("96%",   "Satisfac."),     ("-35%", "Espera"),   ("98%",  "Precisión")],
        "tecnologia":    [("99.9%", "Uptime"),        ("10x",  "Velocidad"),("∞",    "Escala")],
    }
    items = metricas.get(categoria, metricas["tecnologia"])
    cards = "".join(
        f'<div class="nxar-kpi-card">'
        f'<span class="nxar-kpi-val" style="color:{c1}">{v}</span>'
        f'<span class="nxar-kpi-label">{l}</span>'
        f'</div>'
        for v, l in items
    )
    return f'<div class="nxar-kpi-row">{cards}</div>'


# ── Contenido visual por tipo de slide (carrusel) ─────────────────────────────

def _slide_body(tipo: str, s: dict, vis: dict, c1: str, c2: str) -> str:
    titulo = _s(s.get("titulo", ""), 80)
    sub    = _s(s.get("subtitulo", ""), 70)

    if tipo == "portada":
        return (
            '<div style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);'
            'font-size:10px;font-weight:600;color:rgba(255,255,255,0.5);white-space:nowrap;'
            'background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);'
            'border-radius:20px;padding:4px 14px">Desliza &nbsp;›</div>'
        )

    if tipo == "problema":
        sub_li = (
            f'<li style="display:flex;align-items:flex-start;gap:6px">'
            f'<span style="color:#ef4444;font-weight:700;flex-shrink:0">✗</span> {sub}</li>'
        ) if sub else ""
        return (
            f'<div style="width:100%;margin-top:6px">'
            f'<div style="font-size:22px;opacity:0.55;margin-bottom:6px">⚡</div>'
            f'<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:5px;font-size:11px;color:rgba(255,255,255,0.78)">'
            f'<li style="display:flex;align-items:flex-start;gap:6px">'
            f'<span style="color:#ef4444;font-weight:700;flex-shrink:0">✗</span> {titulo}</li>'
            f'{sub_li}'
            f'<li style="display:flex;align-items:flex-start;gap:6px;opacity:0.4">'
            f'<span style="color:#f87171;font-weight:700;flex-shrink:0">✗</span> ¿Te suena familiar?</li>'
            f'</ul>'
            f'<div style="margin-top:8px;font-size:9px;font-weight:700;letter-spacing:0.1em;'
            f'border:1px solid {c1}55;color:{c1};border-radius:4px;padding:3px 9px;display:inline-block">PROBLEMA REAL</div>'
            f'</div>'
        )

    if tipo == "contenido":
        return (
            f'<div style="width:100%;margin-top:6px">'
            f'<div style="width:36px;height:3px;background:linear-gradient(90deg,{c1},{c2});border-radius:2px;margin-bottom:8px"></div>'
            f'<div style="display:flex;gap:6px">'
            f'<div style="flex:1;background:{c1}18;border:1px solid {c1}33;border-radius:6px;padding:6px 8px;font-size:9px;font-weight:600;color:{c1}">◈ Análisis</div>'
            f'<div style="flex:1;background:{c2}18;border:1px solid {c2}33;border-radius:6px;padding:6px 8px;font-size:9px;font-weight:600;color:{c2}">◎ Resultado</div>'
            f'</div>'
            f'<div style="margin-top:8px;opacity:0.65;transform:scale(0.75);transform-origin:left center">{vis["chip"]}</div>'
            f'</div>'
        )

    if tipo == "beneficio":
        sub_li = (
            f'<li style="display:flex;align-items:center;gap:6px">'
            f'<span style="background:{c2};border-radius:50%;width:16px;height:16px;font-size:9px;'
            f'display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff;font-weight:700">✓</span> {sub}</li>'
        ) if sub else ""
        return (
            f'<div style="width:100%;margin-top:6px">'
            f'<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px;font-size:11px;color:rgba(255,255,255,0.88)">'
            f'<li style="display:flex;align-items:center;gap:6px">'
            f'<span style="background:{c1};border-radius:50%;width:16px;height:16px;font-size:9px;'
            f'display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff;font-weight:700">✓</span> {titulo}</li>'
            f'{sub_li}'
            f'<li style="display:flex;align-items:center;gap:6px">'
            f'<span style="background:{c1}88;border-radius:50%;width:16px;height:16px;font-size:9px;'
            f'display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff;font-weight:700">✓</span> Resultados medibles</li>'
            f'</ul>'
            f'<div style="margin-top:8px;box-shadow:0 0 16px {c1}44;background:{c1}18;border:1px solid {c1}55;'
            f'color:{c1};font-size:9px;font-weight:700;letter-spacing:0.1em;border-radius:4px;padding:3px 9px;display:inline-block">BENEFICIO ✓</div>'
            f'</div>'
        )

    if tipo in ("cta", "cierre"):
        return (
            f'<div style="width:100%;margin-top:6px;text-align:center">'
            f'<div style="font-size:9px;font-weight:700;color:{c1};letter-spacing:0.08em;margin-bottom:8px">{vis["icon"]} {vis["label"]}</div>'
            f'<div style="background:linear-gradient(90deg,{c1},{c2});border-radius:20px;padding:8px 20px;font-size:11px;font-weight:700;'
            f'color:#fff;display:inline-block;box-shadow:0 4px 16px {c1}44">{sub or "Contáctanos →"}</div>'
            f'<div style="margin-top:6px;font-size:10px;color:rgba(255,255,255,0.45)">🔗 Link en bio</div>'
            f'</div>'
        )

    return ""


# ── Visual por escena de reel (CapCut style) ─────────────────────────────────

def _escena_visual(tipo: str, vis: dict, c1: str, c2: str, num: int) -> str:
    n = str(num).zfill(2)
    badge = (
        'style="position:absolute;top:8px;right:8px;width:20px;height:20px;'
        'border-radius:50%;display:inline-flex;align-items:center;justify-content:center;'
        'font-size:9px;font-weight:700;color:#fff;'
    )
    if tipo == "hook":
        return (
            f'<div {badge}background:{c1}">{n}</div>'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;margin-bottom:2px">'
            f'{vis["chip"]}'
            f'<div style="font-size:8px;font-weight:700;color:{c1};letter-spacing:0.1em;margin-top:2px">HOOK</div>'
            f'</div>'
        )
    if tipo == "desarrollo":
        return (
            f'<div {badge}background:#475569">{n}</div>'
            f'<div style="width:70%;background:rgba(255,255,255,0.1);border-radius:3px;height:3px;margin:4px auto">'
            f'<div style="width:45%;height:100%;background:{c1};border-radius:3px"></div>'
            f'</div>'
        )
    if tipo == "ejemplo":
        return (
            f'<div {badge}background:#1e3a5f">{n}</div>'
            f'<div style="font-size:8px;font-weight:600;border:1px solid {c2}55;color:{c2};'
            f'padding:2px 5px;border-radius:3px;letter-spacing:0.06em;margin-bottom:2px">DEMO</div>'
            f'{vis["chip"]}'
        )
    if tipo == "cta":
        return (
            f'<div {badge}background:linear-gradient(135deg,{c1},{c2})">{n}</div>'
            f'<div style="font-size:8px;font-weight:700;background:{c1}22;border:1px solid {c1}66;'
            f'color:{c1};padding:2px 6px;border-radius:3px;letter-spacing:0.08em;margin-bottom:2px">CTA FINAL</div>'
        )
    return f'<div {badge}background:#334155">{n}</div>'


def _render_post(empresa, contenido, estructura) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _s(contenido.titulo, 70)
    copy1 = _s(contenido.copy.split("\n")[0], 110)
    cta = _s(contenido.cta or "Contáctanos →", 50)

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)

    return f"""
<div class="nxar-stage nxar-post-stage">
  <div class="nxar-chrome-wrap">
    <div class="nxar-ig-header">
      <div class="nxar-ig-avatar" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
      <div class="nxar-ig-account">
        <span class="nxar-ig-username">{ig_user}</span>
        <span class="nxar-ig-badge">Publicidad</span>
      </div>
      <span class="nxar-ig-dots">⋯</span>
    </div>
    <div class="nxar-post-frame" style="background:linear-gradient(145deg,{c1} 0%,{c2} 100%)">
      <!-- Patrón de fondo -->
      {vis['pattern']}
      <!-- Elemento geométrico -->
      <div class="nxar-geo nxar-geo--circle1" style="background:rgba(255,255,255,0.06)"></div>
      <div class="nxar-geo nxar-geo--circle2" style="background:rgba(255,255,255,0.04)"></div>
      <!-- Hero SVG de categoría -->
      {vis['hero']}
      <!-- Contenido editorial -->
      <div class="nxar-post-content">
        <div class="nxar-post-top">
          <div class="nxar-post-cat-badge">{vis['icon']} {vis['label']}</div>
          <div class="nxar-logo-chip">{_s(nombre, 14)}</div>
        </div>
        <div class="nxar-post-chip-row">
          {vis['chip']}
        </div>
        <div class="nxar-post-body">
          <div style="width:36px;height:3px;background:linear-gradient(90deg,{c1},{c2});border-radius:2px;margin-bottom:6px"></div>
          <h2 class="nxar-post-titulo">{titulo}</h2>
          <p class="nxar-post-copy">{copy1}</p>
          {_kpi_cards(categoria, c1)}
        </div>
        <div class="nxar-post-bottom">
          <div class="nxar-post-cta" style="background:rgba(255,255,255,0.92);color:{c1};text-shadow:none;font-weight:800">{cta}</div>
          <div class="nxar-post-cta-arrow" style="color:rgba(255,255,255,0.6)">→</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span>
        <span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span>
        <span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">3,241 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {copy1[:60]}...</div>
    </div>
  </div>
</div>"""


def _render_historia(empresa, contenido, estructura) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    pantallas = estructura.get("pantallas", [])

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)

    sticker_html = {
        "encuesta": lambda color: f'<div class="nxar-sticker nxar-sticker--encuesta"><span>¿Qué opinas?</span><div class="nxar-encuesta-op" style="border-color:{color};background:{color}22">Sí 👍</div><div class="nxar-encuesta-op">No 👎</div></div>',
        "deslizador": lambda color: f'<div class="nxar-sticker nxar-sticker--deslizador">Reacciona 😍<div class="nxar-deslizador-track"><div class="nxar-deslizador-thumb" style="background:{color}">😍</div></div></div>',
        "link": lambda color: f'<div class="nxar-sticker nxar-sticker--link" style="border-color:{color};color:{color}">🔗 Ver más</div>',
    }

    # Fondos por pantalla: gradiente marca → oscuro con acento → muy oscuro
    bg_pantallas = [
        f"linear-gradient(145deg,{c1},{c2})",
        f"linear-gradient(160deg,{c2}cc,#0f172a)",
        "#0f172a",
    ]

    screens_html = ""
    total = len(pantallas) or 3
    for i, p in enumerate(pantallas[:3]):
        bg = bg_pantallas[i] if i < len(bg_pantallas) else bg_pantallas[-1]
        sk = p.get("sticker", "link")
        sk_fn = sticker_html.get(sk, sticker_html["link"])
        dur = p.get("duracion", "7s")

        hero_el = vis["hero"] if i == 0 else ""
        extra_vis = ""
        if i == 1:
            extra_vis = (
                f'<div style="width:80%;background:rgba(255,255,255,0.12);border-radius:4px;height:3px;margin:0 auto 6px">'
                f'<div style="width:60%;height:100%;background:{c1};border-radius:4px"></div>'
                f'</div>'
                f'<div style="display:flex;justify-content:center;margin-bottom:4px;opacity:0.65;transform:scale(0.8);transform-origin:center">{vis["chip"]}</div>'
            )
        elif i == 2:
            extra_vis = (
                f'<div style="background:linear-gradient(90deg,{c1},{c2});border-radius:20px;'
                f'padding:7px 16px;font-size:11px;font-weight:700;color:#fff;'
                f'display:inline-block;margin-bottom:8px;box-shadow:0 4px 14px {c1}44">Ver más →</div>'
            )

        screens_html += f"""
    <div class="nxar-story-screen" style="background:{bg}">
      {vis['pattern']}
      {hero_el}
      <div class="nxar-story-bars">
        {"".join(f'<div class="nxar-story-bar {"nxar-story-bar--done" if j < i else "nxar-story-bar--active" if j == i else ""}"></div>' for j in range(total))}
      </div>
      <div class="nxar-story-account">
        <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
        <span class="nxar-story-username">{_s(nombre, 20)}</span>
        <span class="nxar-story-time">{dur}</span>
        <span class="nxar-story-x">✕</span>
      </div>
      <div class="nxar-story-cat-tag">{vis['icon']} {vis['label']}</div>
      <div class="nxar-story-body">
        <p class="nxar-story-titulo">{_s(p.get('titulo', ''), 80)}</p>
        {f'<p class="nxar-story-sub">{_s(p.get("subtitulo",""),60)}</p>' if p.get("subtitulo") else ""}
        {extra_vis}
        {sk_fn(c1)}
      </div>
      <div class="nxar-story-bottom">
        <div class="nxar-story-reply">Responder...</div>
        <span class="nxar-story-share">↗</span>
      </div>
    </div>"""

    return f"""
<div class="nxar-stage nxar-historia-stage">
  <div class="nxar-historia-wrap">{screens_html}</div>
</div>"""


def _render_carrusel(empresa, contenido, estructura) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    slides = estructura.get("slides", [])
    total = len(slides)

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)
    accents = vis["slide_accent"]

    tipo_bg = {
        "portada":   f"linear-gradient(145deg,{c1},{c2})",
        "problema":  "linear-gradient(145deg,#1e1028,#16213e)",
        "contenido": "linear-gradient(145deg,#0d1b2e,#16213e)",
        "beneficio": "linear-gradient(145deg,#0d2137,#0a1628)",
        "cierre":    "linear-gradient(145deg,#12203a,#0d1b2e)",
        "cta":       f"linear-gradient(145deg,{c2},{c1})",
    }
    tipo_icon = {
        "portada": vis["icon"], "problema": "⚡", "contenido": "◈",
        "beneficio": "✓", "cierre": "→", "cta": "★",
    }

    slides_html = ""
    for i, s in enumerate(slides):
        tipo = s.get("tipo", "contenido")
        bg = tipo_bg.get(tipo, "linear-gradient(145deg,#1a1a2e,#0f172a)")
        icon = tipo_icon.get(tipo, vis["icon"])
        active = "nxar-slide--active" if i == 0 else ""
        accent_html = accents.get(tipo, "")

        # Slide portada recibe el hero SVG de la categoría
        hero_html = vis["hero"] if tipo == "portada" else ""
        pattern_html = vis["pattern"] if tipo in ("portada", "cta") else _pattern_grid()

        slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg}">
      {pattern_html}
      <div class="nxar-geo nxar-geo--circle1" style="background:rgba(255,255,255,0.04)"></div>
      {hero_html}
      {accent_html}
      <div class="nxar-slide-content">
        <div class="nxar-slide-header">
          <div class="nxar-slide-tipo-badge">{tipo.upper()}</div>
          <div class="nxar-slide-counter">{i+1}/{total}</div>
        </div>
        <div class="nxar-slide-icon" style="color:{c1};font-size:{'40px' if tipo=='portada' else '28px'}">{icon}</div>
        <h2 class="nxar-slide-titulo" style="font-size:{'clamp(18px,3.5vw,26px)' if tipo=='portada' else 'clamp(15px,3vw,22px)'}">{_s(s.get('titulo', ''), 80)}</h2>
        {f'<p class="nxar-slide-sub">{_s(s.get("subtitulo",""),70)}</p>' if s.get("subtitulo") else ''}
        {f'<div class="nxar-slide-chip" style="border-color:{c1}33;color:{c1}">{vis["label"]}</div>' if tipo == "portada" else ''}
        {_slide_body(tipo, s, vis, c1, c2)}
      </div>
      {f'<div class="nxar-slide-logo" style="color:rgba(255,255,255,0.25)">{_s(nombre,14)}</div>' if i == 0 or i == total-1 else ''}
    </div>"""

    dots_html = "".join(
        f'<span class="nxar-dot {"nxar-dot--active" if i == 0 else ""}" data-dot="{i}"></span>'
        for i in range(total)
    )

    return f"""
<div class="nxar-stage nxar-carrusel-stage" id="nxarCarrusel">
  <!-- Header Instagram -->
  <div class="nxar-ig-header">
    <div class="nxar-ig-avatar" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
    <div class="nxar-ig-account">
      <span class="nxar-ig-username">{ig_user}</span>
    </div>
    <span class="nxar-ig-dots">⋯</span>
  </div>
  <!-- Slides -->
  <div class="nxar-slides-container">
    <button class="nxar-nav-btn nxar-nav-btn--prev" onclick="nxarNav(-1)" aria-label="anterior">‹</button>
    <div class="nxar-slides-track">{slides_html}</div>
    <button class="nxar-nav-btn nxar-nav-btn--next" onclick="nxarNav(1)" aria-label="siguiente">›</button>
  </div>
  <!-- Dots -->
  <div class="nxar-dots">{dots_html}</div>
  <!-- Footer Instagram -->
  <div class="nxar-ig-footer">
    <div class="nxar-ig-actions">
      <span class="nxar-ig-action">♡</span>
      <span class="nxar-ig-action">💬</span>
      <span class="nxar-ig-action">↗</span>
      <span class="nxar-ig-action nxar-ig-action--right">🔖</span>
    </div>
    <div class="nxar-ig-likes">2,891 Me gusta</div>
  </div>
</div>
<script>
(function(){{
  var cur = 0;
  window.nxarNav = function(dir) {{
    var slides = document.querySelectorAll('#nxarCarrusel .nxar-slide');
    var dots   = document.querySelectorAll('#nxarCarrusel .nxar-dot');
    if (!slides.length) return;
    slides[cur].classList.remove('nxar-slide--active');
    dots[cur] && dots[cur].classList.remove('nxar-dot--active');
    cur = (cur + dir + slides.length) % slides.length;
    slides[cur].classList.add('nxar-slide--active');
    dots[cur] && dots[cur].classList.add('nxar-dot--active');
  }};
  document.querySelectorAll('#nxarCarrusel .nxar-dot').forEach(function(d) {{
    d.addEventListener('click', function() {{
      var t = parseInt(d.dataset.dot);
      nxarNav(t - cur);
    }});
  }});
}})();
</script>"""


def _render_reel(empresa, contenido, estructura) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    escenas = estructura.get("escenas", [])
    hook_txt = _s(estructura.get("hook", contenido.titulo), 80)
    duracion = estructura.get("duracion_total", "30s")

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)

    tipo_bg = {
        "hook":       f"linear-gradient(145deg,{c1},{c2})",
        "desarrollo": "linear-gradient(145deg,#1e1028,#16213e)",
        "ejemplo":    "linear-gradient(145deg,#0d1b2e,#16213e)",
        "cta":        f"linear-gradient(145deg,{c2},{c1})",
    }
    tipo_label = {
        "hook": "HOOK", "desarrollo": "DESARROLLO", "ejemplo": "EJEMPLO", "cta": "CTA",
    }
    transicion_sym = {"corte": "✦", "fundido": "◌"}

    escenas_html = ""
    for e in escenas:
        tipo = e.get("tipo", "desarrollo")
        bg = tipo_bg.get(tipo, "linear-gradient(145deg,#1a1a2e,#16213e)")
        label = tipo_label.get(tipo, tipo.upper())
        rango = _s(e.get("rango", ""), 10)
        trans = e.get("transicion", "corte")
        trans_sym = transicion_sym.get(trans, "•")

        num = e.get("numero", escenas.index(e) + 1)
        escenas_html += f"""
    <div class="nxar-escena">
      <div class="nxar-escena-frame" style="background:{bg}">
        {vis["pattern"] if tipo in ("hook", "cta") else ""}
        <span class="nxar-escena-label">{label}</span>
        {_escena_visual(tipo, vis, c1, c2, num)}
        <p class="nxar-escena-texto">{_s(e.get('texto', ''), 60)}</p>
      </div>
      <div class="nxar-escena-meta">
        <span class="nxar-escena-rango">⏱ {rango}</span>
        <span class="nxar-escena-trans" title="{trans}">{trans_sym}</span>
      </div>
    </div>"""

    return f"""
<div class="nxar-stage nxar-reel-stage">
  <div class="nxar-reel-header" style="background:linear-gradient(135deg,{c1}22,{c2}22);border-color:{c1}33">
    <div class="nxar-reel-meta">
      <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
      <span class="nxar-reel-nombre">{_s(nombre, 20)}</span>
      <span class="nxar-reel-cat" style="color:{c1}">{vis['icon']} {vis['label']}</span>
      <span class="nxar-reel-dur">🎬 {duracion}</span>
    </div>
    <div class="nxar-reel-hook-txt">"{hook_txt}"</div>
  </div>
  <div class="nxar-reel-timeline-label">STORYBOARD · {len(escenas)} escenas</div>
  <!-- Escenas grid -->
  <div class="nxar-escenas-grid">{escenas_html}</div>
  <!-- Footer acciones -->
  <div class="nxar-reel-footer">
    <div class="nxar-reel-actions">
      <span>♡ 4.2k</span>
      <span>💬 183</span>
      <span>↗ Compartir</span>
    </div>
  </div>
</div>"""
