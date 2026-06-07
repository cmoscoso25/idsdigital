"""
Agente Diseño Instagram — Nexa AI
Genera creatividades visuales profesionales para Instagram.
Motor de Estilos Creativos: cada pieza usa un estilo diferente según el Director Creativo.

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


from nexa.services.agentes.director_creativo import seleccionar_estilo  # noqa: E402
from nexa.services.visual_assets import get_visual_pack, get_slide_visual  # noqa: E402


def _tw(text: str, max_words: int, maxlen: int = 100) -> str:
    """Trunca texto a max_words palabras (regla Instagram: títulos breves)."""
    words = str(text or "").split()
    out = " ".join(words[:max_words])
    if len(words) > max_words:
        out += "..."
    return _s(out, maxlen)


def _afs(text: str, fmt: str = "slide") -> str:
    """Retorna un valor CSS font-size adaptado a la longitud del texto.

    Reduce el tamaño progresivamente para que títulos largos no rompan el layout.
    La CSS ya aplica overflow-wrap y line-clamp como segunda capa de seguridad.
    """
    n = len(str(text or ""))
    _table = {
        "post":  [(20, "clamp(17px,3.4vw,22px)"), (45, "clamp(14px,2.8vw,18px)"),
                  (70, "clamp(12px,2.3vw,15px)"), (9999, "clamp(11px,2vw,13px)")],
        "slide": [(20, "clamp(16px,3.2vw,22px)"), (45, "clamp(13px,2.5vw,18px)"),
                  (70, "clamp(11px,2vw,14px)"),   (9999, "clamp(10px,1.8vw,12px)")],
        "story": [(25, "14px"), (45, "13px"), (65, "12px"), (9999, "11px")],
        "reel":  [(25, "12px"), (45, "11px"), (9999, "10px")],
    }
    for threshold, size in _table.get(fmt, _table["slide"]):
        if n <= threshold:
            return size
    return _table.get(fmt, _table["slide"])[-1][1]


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

    categoria = _detectar_categoria(contenido, empresa)
    estilo = seleccionar_estilo("post", empresa, contenido)
    estructura["estilo_creativo"] = {"id": estilo["id"], "nombre": estilo["nombre"]}

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_post(empresa, contenido, estructura, estilo),
        "render_css": "",
        "estilo": estilo["id"],
        "estilo_nombre": estilo["nombre"],
        "categoria_visual": categoria,
        "motivo_seleccion": estilo.get("motivo_seleccion", ""),
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

    categoria = _detectar_categoria(contenido, empresa)
    estilo = seleccionar_estilo("historia", empresa, contenido)
    estructura["estilo_creativo"] = {"id": estilo["id"], "nombre": estilo["nombre"]}

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_historia(empresa, contenido, estructura, estilo),
        "render_css": "",
        "estilo": estilo["id"],
        "estilo_nombre": estilo["nombre"],
        "categoria_visual": categoria,
        "motivo_seleccion": estilo.get("motivo_seleccion", ""),
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

    categoria = _detectar_categoria(contenido, empresa)
    estilo = seleccionar_estilo("carrusel", empresa, contenido)
    estructura["estilo_creativo"] = {"id": estilo["id"], "nombre": estilo["nombre"]}

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_carrusel(empresa, contenido, estructura, estilo),
        "render_css": "",
        "estilo": estilo["id"],
        "estilo_nombre": estilo["nombre"],
        "categoria_visual": categoria,
        "motivo_seleccion": estilo.get("motivo_seleccion", ""),
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

    categoria = _detectar_categoria(contenido, empresa)
    estilo = seleccionar_estilo("reel", empresa, contenido)
    estructura["estilo_creativo"] = {"id": estilo["id"], "nombre": estilo["nombre"]}

    return {
        "prompt_visual": prompt_visual,
        "estructura_visual_json": estructura,
        "render_html": _render_reel(empresa, contenido, estructura, estilo),
        "render_css": "",
        "estilo": estilo["id"],
        "estilo_nombre": estilo["nombre"],
        "categoria_visual": categoria,
        "motivo_seleccion": estilo.get("motivo_seleccion", ""),
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

    if tipo == "consecuencia":
        sub_li = (
            f'<li style="display:flex;align-items:flex-start;gap:6px">'
            f'<span style="color:#f59e0b;font-weight:700;flex-shrink:0">⚠</span> {sub}</li>'
        ) if sub else ""
        return (
            f'<div style="width:100%;margin-top:6px">'
            f'<div style="font-size:22px;opacity:0.6;margin-bottom:6px">⚠️</div>'
            f'<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:5px;font-size:11px;color:rgba(255,255,255,0.78)">'
            f'<li style="display:flex;align-items:flex-start;gap:6px">'
            f'<span style="color:#f59e0b;font-weight:700;flex-shrink:0">⚠</span> {titulo}</li>'
            f'{sub_li}'
            f'<li style="display:flex;align-items:flex-start;gap:6px;opacity:0.4">'
            f'<span style="color:#fbbf24;font-weight:700;flex-shrink:0">⚠</span> El costo de no actuar</li>'
            f'</ul>'
            f'<div style="margin-top:8px;font-size:9px;font-weight:700;letter-spacing:0.1em;'
            f'border:1px solid #f59e0b55;color:#f59e0b;border-radius:4px;padding:3px 9px;display:inline-block">IMPACTO REAL</div>'
            f'</div>'
        )

    if tipo == "solucion":
        return (
            f'<div style="width:100%;margin-top:6px">'
            f'<div style="font-size:22px;opacity:0.6;margin-bottom:6px">✓</div>'
            f'<div style="background:{c1}18;border:1px solid {c1}44;border-radius:8px;padding:8px 10px;'
            f'font-size:11px;color:rgba(255,255,255,0.85);margin-bottom:6px;line-height:1.4">{titulo}</div>'
            f'<div style="width:36px;height:3px;background:linear-gradient(90deg,{c1},{c2});border-radius:2px;margin:4px 0"></div>'
            f'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;'
            f'color:{c1};display:inline-block">SOLUCIÓN PROBADA</div>'
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
    if tipo == "problema":
        return (
            f'<div {badge}background:#b45309">{n}</div>'
            f'<div style="font-size:8px;font-weight:700;color:#f59e0b;letter-spacing:0.08em;margin-bottom:2px">⚡ PROBLEMA</div>'
        )
    if tipo in ("desarrollo", "solucion"):
        bar_pct = "45%" if tipo == "desarrollo" else "75%"
        label   = "SOLUCIÓN" if tipo == "solucion" else "DESARROLLO"
        return (
            f'<div {badge}background:#1e3a5f">{n}</div>'
            f'<div style="font-size:8px;font-weight:700;color:{c1};letter-spacing:0.08em;margin-bottom:3px">{label}</div>'
            f'<div style="width:70%;background:rgba(255,255,255,0.1);border-radius:3px;height:3px;margin:0 auto">'
            f'<div style="width:{bar_pct};height:100%;background:{c1};border-radius:3px"></div>'
            f'</div>'
        )
    if tipo in ("ejemplo", "beneficio"):
        label = "RESULTADO" if tipo == "beneficio" else "DEMO"
        color = c1 if tipo == "beneficio" else c2
        return (
            f'<div {badge}background:#1e3a5f">{n}</div>'
            f'<div style="font-size:8px;font-weight:600;border:1px solid {color}55;color:{color};'
            f'padding:2px 5px;border-radius:3px;letter-spacing:0.06em;margin-bottom:2px">{label}</div>'
            f'{vis["chip"]}'
        )
    if tipo == "cta":
        return (
            f'<div {badge}background:linear-gradient(135deg,{c1},{c2})">{n}</div>'
            f'<div style="font-size:8px;font-weight:700;background:{c1}22;border:1px solid {c1}66;'
            f'color:{c1};padding:2px 6px;border-radius:3px;letter-spacing:0.08em;margin-bottom:2px">CTA FINAL</div>'
        )
    return f'<div {badge}background:#334155">{n}</div>'


def _render_post(empresa, contenido, estructura, estilo=None) -> str:
    """Dispatcher — delega al renderer del estilo seleccionado."""
    estilo_id = (estilo or {}).get("id", "corporate_kpi")
    _dispatch = {
        "corporate_kpi":       _render_post_corporate_kpi,
        "minimalista_premium": _render_post_minimalista,
        "problema_solucion":   _render_post_problema_solucion,
        "estadistica":         _render_post_estadistica,
        "testimonio":          _render_post_testimonio,
        "startup_saas":        _render_post_startup_saas,
        "tech_futurista":      _render_post_tech_futurista,
        "ia_neural":           _render_post_ia_neural,
        "dashboard_analytics": _render_post_dashboard_analytics,
        "modern_gradient":     _render_post_modern_gradient,
    }
    return _dispatch.get(estilo_id, _render_post_corporate_kpi)(empresa, contenido, estructura)


def _render_post_corporate_kpi(empresa, contenido, estructura) -> str:
    """Ilustración hero grande (55%) + KPI cards + texto breve (45%). Layout B2B premium."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 8)
    cta = _s(contenido.cta or "Ver más →", 40)
    categoria = _detectar_categoria(contenido, empresa)
    vpack = get_visual_pack(categoria, c1, c2)

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
    <div class="nxar-post-frame" style="background:#04060e;position:relative;overflow:hidden;aspect-ratio:1/1;display:flex;flex-direction:column">
      <!-- ZONA VISUAL (58%) -->
      <div style="flex:0 0 58%;position:relative;overflow:hidden;background:linear-gradient(160deg,#06080f,#080c18)">
        {vpack['hero']}
        <!-- Overlay gradiente al pie de la zona visual -->
        <div style="position:absolute;bottom:0;left:0;right:0;height:40%;background:linear-gradient(transparent,#04060e)"></div>
        <!-- Badge categoría flotante -->
        <div style="position:absolute;top:10px;left:12px;font-size:8px;font-weight:700;letter-spacing:0.12em;color:{c1};background:{c1}18;border:1px solid {c1}44;border-radius:4px;padding:3px 8px">{_s(categoria.upper(),20)}</div>
        <!-- Logo chip -->
        <div style="position:absolute;top:10px;right:12px;font-size:9px;font-weight:700;color:rgba(255,255,255,0.7);background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:12px;padding:3px 9px">{_s(nombre,14)}</div>
      </div>
      <!-- ZONA TEXTO (42%) -->
      <div style="flex:1;padding:12px 16px;display:flex;flex-direction:column;justify-content:space-between;background:#04060e">
        <div>
          <div style="width:28px;height:2px;background:linear-gradient(90deg,{c1},{c2});border-radius:1px;margin-bottom:6px"></div>
          <h2 style="font-size:{_afs(titulo,'post')};font-weight:900;color:#fff;line-height:1.15;letter-spacing:-0.03em;margin:0 0 4px">{titulo}</h2>
          {_kpi_cards(categoria, c1)}
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px">
          <div style="background:rgba(255,255,255,0.9);color:{c1};border-radius:18px;padding:5px 14px;font-size:10px;font-weight:800">{cta}</div>
          <div style="font-size:10px;color:rgba(255,255,255,0.3);font-weight:600">{_s(nombre,12)}</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">3,241 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


# ── POST: 4 estilos adicionales ───────────────────────────────────────────────

def _render_post_minimalista(empresa, contenido, estructura) -> str:
    """Visual hero izquierda (45%) + tipografía masiva derecha (55%). Layout editorial premium."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 8)
    subtitulo = _tw(contenido.copy.split("\n")[0], 14)
    cta = _s(contenido.cta or "Descubrir →", 35)
    categoria = _detectar_categoria(contenido, empresa)
    vpack = get_visual_pack(categoria, c1, c2)

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
    <div class="nxar-post-frame" style="background:#070508;position:relative;overflow:hidden;aspect-ratio:1/1;display:flex;flex-direction:row">
      <!-- COLUMNA VISUAL (45%) -->
      <div style="width:45%;position:relative;overflow:hidden;background:linear-gradient(160deg,#050308,#090710)">
        {vpack['hero']}
        <div style="position:absolute;inset:0;background:linear-gradient(to right,transparent 60%,#070508)"></div>
        <div style="position:absolute;bottom:16px;left:12px;font-size:8px;font-weight:700;letter-spacing:0.14em;color:{c1};background:{c1}18;border:1px solid {c1}33;border-radius:4px;padding:2px 7px">{_s(categoria.upper(),18)}</div>
      </div>
      <!-- COLUMNA TEXTO (55%) -->
      <div style="flex:1;display:flex;flex-direction:column;justify-content:space-between;padding:18px 16px 16px 12px">
        <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.25);letter-spacing:0.1em">{_s(nombre,14)}</div>
        <div>
          <div style="width:24px;height:2px;background:{c1};border-radius:1px;margin-bottom:10px"></div>
          <h2 style="font-size:{_afs(titulo,'post')};font-weight:900;color:#fff;line-height:1.1;letter-spacing:-0.04em;margin:0 0 8px">{titulo}</h2>
          <p style="font-size:10px;color:rgba(255,255,255,0.5);line-height:1.5;margin:0">{subtitulo}</p>
        </div>
        <div>
          <div style="width:100%;height:1px;background:rgba(255,255,255,0.07);margin-bottom:10px"></div>
          <div style="font-size:10px;font-weight:700;color:{c1};letter-spacing:0.06em">{cta} →</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">2,817 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_post_problema_solucion(empresa, contenido, estructura) -> str:
    """Split LEFT/RIGHT: problema (40%) | solución (60%). Contraste total."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _s(contenido.titulo, 70)
    copy1 = _s(contenido.copy.split("\n")[0], 90)
    cta = _s(contenido.cta or "Contáctanos →", 40)
    secciones = estructura.get("secciones", [])
    problema_txt = next((s["texto"] for s in secciones if s.get("tipo") == "hook"), titulo)
    solucion_txt = next((s["texto"] for s in secciones if s.get("tipo") == "beneficio"), copy1)
    prueba_txt   = next((s["texto"] for s in secciones if s.get("tipo") == "prueba"), "")

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
    <div class="nxar-post-frame" style="position:relative;overflow:hidden;aspect-ratio:1/1;display:flex;flex-direction:row">
      <!-- COLUMNA IZQUIERDA: PROBLEMA (38%) -->
      <div style="width:38%;background:#100812;display:flex;flex-direction:column;padding:16px 12px 16px 14px;position:relative;border-right:2px solid {c1}88">
        <div style="font-size:8px;font-weight:900;letter-spacing:0.18em;color:#ef4444;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.25);border-radius:3px;padding:2px 6px;display:inline-block;margin-bottom:10px">⚡ PROBLEMA</div>
        <p style="font-size:clamp(11px,2vw,13px);font-weight:700;color:rgba(255,255,255,0.85);line-height:1.4;flex:1;margin:0">{_s(problema_txt,75)}</p>
        <div style="margin-top:10px;font-size:36px;opacity:0.1;color:#ef4444;line-height:1">?</div>
        <div style="font-size:8px;color:rgba(255,255,255,0.2);margin-top:6px">{_s(nombre,12)}</div>
      </div>
      <!-- DIVISOR con flecha central -->
      <div style="width:0;position:relative;z-index:3">
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:22px;height:22px;background:linear-gradient(135deg,{c1},{c2});border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;box-shadow:0 0 10px {c1}88">→</div>
      </div>
      <!-- COLUMNA DERECHA: SOLUCIÓN (62%) -->
      <div style="flex:1;background:linear-gradient(160deg,{c1}22,{c2}18,#06060e);display:flex;flex-direction:column;padding:16px 14px 16px 18px;position:relative;overflow:hidden">
        <div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;background:radial-gradient({c1}33,transparent 70%);border-radius:50%"></div>
        <div style="font-size:8px;font-weight:900;letter-spacing:0.18em;color:{c1};background:{c1}14;border:1px solid {c1}33;border-radius:3px;padding:2px 6px;display:inline-block;margin-bottom:10px">✓ SOLUCIÓN</div>
        <p style="font-size:clamp(11px,2vw,13px);font-weight:600;color:rgba(255,255,255,0.9);line-height:1.45;flex:1;margin:0">{_s(solucion_txt,90)}</p>
        {f'<p style="font-size:9px;color:{c1};margin:8px 0 0;line-height:1.35;opacity:0.8">{_s(prueba_txt,65)}</p>' if prueba_txt else ""}
        <div style="margin-top:10px;background:linear-gradient(90deg,{c1},{c2});border-radius:16px;padding:5px 12px;font-size:9px;font-weight:800;color:#fff;display:inline-block;align-self:flex-start">{cta}</div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">4,102 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {_s(problema_txt,55)}...</div>
    </div>
  </div>
</div>"""


def _render_post_estadistica(empresa, contenido, estructura) -> str:
    """Número hero gigante + 3 barras de progreso visuales con métricas."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _s(contenido.titulo, 70)
    copy1 = _s(contenido.copy.split("\n")[0], 100)
    cta = _s(contenido.cta or "Ver datos →", 45)
    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)

    import re as _re
    stat_match = _re.search(r'(\d+[\d.,]*\s*[%xX×]?)', titulo)
    stat_num = stat_match.group(1) if stat_match else "10x"
    stat_ctx = (titulo.replace(stat_match.group(0), "").strip() if stat_match else titulo)[:55]

    # KPIs para barras (por categoría)
    _kpi_bars = {
        "ia":            [("98%", "Precisión"), ("73%", "Tiempo ↓"), ("4.2x", "ROI")],
        "software":      [("99.9%", "Uptime"), ("87%", "Satisf."), ("3x", "Velocidad")],
        "marketing":     [("+48%", "Tráfico"), ("+32%", "Convers."), ("6x", "ROAS")],
        "automatizacion":[("85%", "Automati."), ("10x", "Velocidad"), ("0%", "Errores")],
        "productividad": [("70%", "Eficienc."), ("8h/sem", "Ahorro"), ("3x", "Output")],
    }
    bars_data = _kpi_bars.get(categoria, [("73%", "Eficiencia"), ("+40%", "Resultados"), ("10x", "ROI")])
    # Convertir el valor a % para la barra visual
    def _bar_pct(val: str) -> int:
        import re
        m = re.search(r'(\d+)', val)
        if m:
            v = int(m.group(1))
            return min(v, 100) if "%" in val else min(v * 10, 95)
        return 70
    bars_html = "".join(
        f'<div style="margin-bottom:6px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
        f'<span style="font-size:9px;color:rgba(255,255,255,0.55)">{label}</span>'
        f'<span style="font-size:10px;font-weight:700;color:{c1}">{val}</span>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.07);border-radius:3px;height:5px">'
        f'<div style="width:{_bar_pct(val)}%;height:100%;background:linear-gradient(90deg,{c1},{c2});border-radius:3px"></div>'
        f'</div>'
        f'</div>'
        for val, label in bars_data
    )

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
    <div class="nxar-post-frame" style="background:linear-gradient(160deg,#04010c,#0c0818);position:relative;overflow:hidden;aspect-ratio:1/1">
      {vis['pattern']}
      <div style="position:absolute;top:-30px;left:-30px;width:120px;height:120px;background:radial-gradient({c1}22,transparent 70%);border-radius:50%"></div>
      <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:18px 20px">
        <!-- Header -->
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:9px;font-weight:700;color:{c1};letter-spacing:0.12em;text-transform:uppercase">{vis['icon']} ESTADÍSTICA</span>
          <span style="font-size:9px;color:rgba(255,255,255,0.18)">{_s(nombre,12)}</span>
        </div>
        <!-- Hero number -->
        <div style="display:flex;align-items:flex-end;gap:8px;padding:4px 0">
          <div style="font-size:clamp(52px,11vw,80px);font-weight:900;color:{c1};line-height:0.9;letter-spacing:-0.05em;text-shadow:0 0 32px {c1}99">{stat_num}</div>
          <div style="padding-bottom:8px">
            <p style="font-size:11px;color:rgba(255,255,255,0.75);margin:0;line-height:1.3;max-width:110px">{stat_ctx}</p>
            <p style="font-size:9px;color:rgba(255,255,255,0.3);margin:2px 0 0">Fuente: {_s(nombre,16)}</p>
          </div>
        </div>
        <!-- Barras de progreso -->
        <div style="border-top:1px solid rgba(255,255,255,0.07);padding-top:10px">
          {bars_html}
        </div>
        <!-- CTA -->
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div style="background:linear-gradient(90deg,{c1}33,{c2}22);border:1px solid {c1}44;border-radius:20px;padding:5px 14px;font-size:10px;font-weight:700;color:{c1}">{cta}</div>
          <div style="opacity:0.55;transform:scale(0.7);transform-origin:right">{vis['chip']}</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">5,448 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {copy1[:60]}...</div>
    </div>
  </div>
</div>"""


def _render_post_testimonio(empresa, contenido, estructura) -> str:
    """Tarjeta de caso de éxito: resultado destacado + cita + atribución."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _s(contenido.titulo, 75)
    copy1 = _s(contenido.copy.split("\n")[0], 110)
    cta = _s(contenido.cta or "Ver caso completo →", 45)

    # Extraer métrica de resultado del título o copy
    import re as _re
    m = _re.search(r'(\d+[\d.,]*\s*[%xX×])', contenido.titulo + " " + contenido.copy[:100])
    resultado_num = m.group(1) if m else "+40%"

    # Obtener cliente/servicio del contenido
    lineas = [l.strip() for l in contenido.copy.split("\n") if l.strip()]
    quote_txt = lineas[0][:80] if lineas else titulo[:80]

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
    <div class="nxar-post-frame" style="background:linear-gradient(155deg,#050310,#0e0918);position:relative;overflow:hidden;aspect-ratio:1/1">
      <!-- Glow de acento -->
      <div style="position:absolute;bottom:-40px;right:-40px;width:150px;height:150px;background:radial-gradient({c1}22,transparent 70%);border-radius:50%"></div>
      <!-- Borde superior de color -->
      <div style="position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,{c1},{c2})"></div>
      <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;padding:20px 20px 16px">
        <!-- Tarjeta de resultado (hero element) -->
        <div style="background:linear-gradient(135deg,{c1}22,{c2}14);border:1px solid {c1}44;border-radius:10px;padding:10px 14px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between">
          <div>
            <div style="font-size:8px;font-weight:700;letter-spacing:0.15em;color:rgba(255,255,255,0.45);text-transform:uppercase;margin-bottom:2px">Resultado obtenido</div>
            <div style="font-size:clamp(22px,5vw,32px);font-weight:900;color:{c1};line-height:1;letter-spacing:-0.03em">{resultado_num}</div>
          </div>
          <div style="font-size:9px;font-weight:700;color:{c1};background:{c1}18;border:1px solid {c1}33;border-radius:16px;padding:4px 10px">CASO REAL</div>
        </div>
        <!-- Comillas decorativas + cita -->
        <div style="flex:1;position:relative;padding:0 4px">
          <div style="position:absolute;top:-8px;left:-2px;font-size:44px;font-weight:900;color:{c1};opacity:0.2;line-height:1;font-family:Georgia,serif">"</div>
          <p style="font-size:clamp(12px,2.2vw,14px);font-style:italic;color:rgba(255,255,255,0.85);line-height:1.5;margin:0;padding-left:14px">{_s(quote_txt,90)}</p>
        </div>
        <!-- Atribución -->
        <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:10px;display:flex;align-items:center;justify-content:space-between">
          <div style="display:flex;align-items:center;gap:8px">
            <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,{c1},{c2});display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:12px;flex-shrink:0">{initial}</div>
            <div>
              <p style="margin:0;font-size:10px;font-weight:700;color:#fff">{_s(nombre,20)}</p>
              <p style="margin:0;font-size:8px;color:rgba(255,255,255,0.4)">Caso de éxito</p>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:4px 10px;font-size:8px;font-weight:600;color:rgba(255,255,255,0.55)">{cta[:30]}</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">3,760 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {copy1[:60]}...</div>
    </div>
  </div>
</div>"""


def _render_post_startup_saas(empresa, contenido, estructura) -> str:
    """Layout vertical: banda superior de color + área texto + badge flotante con métrica."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 7)
    subtitulo = _s(contenido.copy.split("\n")[0], 80)
    cta = _s(contenido.cta or "Probar gratis →", 35)
    secciones = estructura.get("secciones", [])
    prueba = next((s["texto"] for s in secciones if s.get("tipo") == "prueba"), "")
    import re as _re2
    m = _re2.search(r'(\d+[\d.,]*\s*[%xX×kdm]?)', prueba or titulo)
    badge_num = m.group(1) if m else "10x"

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
    <div class="nxar-post-frame" style="background:#0a0a10;position:relative;overflow:hidden;aspect-ratio:1/1;display:flex;flex-direction:column">
      <!-- BANDA SUPERIOR DE COLOR (35%) -->
      <div style="flex:0 0 35%;background:linear-gradient(125deg,{c1},{c2});position:relative;overflow:hidden">
        <!-- Patrón de puntos -->
        <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.15" xmlns="http://www.w3.org/2000/svg">
          <defs><pattern id="ss_dots" x="0" y="0" width="18" height="18" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.5" fill="#fff"/>
          </pattern></defs>
          <rect width="100%" height="100%" fill="url(#ss_dots)"/>
        </svg>
        <!-- Badge flotante -->
        <div style="position:absolute;top:14px;right:16px;background:rgba(0,0,0,0.35);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,0.3);border-radius:20px;padding:5px 12px;display:flex;align-items:center;gap:6px">
          <div style="font-size:18px;font-weight:900;color:#fff;line-height:1">{badge_num}</div>
          <div style="font-size:7px;font-weight:700;color:rgba(255,255,255,0.8);line-height:1.2">más<br>rápido</div>
        </div>
        <!-- Wordmark -->
        <div style="position:absolute;bottom:12px;left:14px;font-size:11px;font-weight:800;color:rgba(255,255,255,0.9);letter-spacing:-0.02em">{_s(nombre,16)}</div>
      </div>
      <!-- ÁREA TEXTO (65%) -->
      <div style="flex:1;padding:16px 18px 14px;display:flex;flex-direction:column;justify-content:space-between">
        <div>
          <div style="font-size:8px;font-weight:700;letter-spacing:0.12em;color:{c1};margin-bottom:8px">✦ NUEVO</div>
          <h2 style="font-size:{_afs(titulo,'post')};font-weight:900;color:#fff;line-height:1.1;letter-spacing:-0.04em;margin:0 0 8px">{titulo}</h2>
          <p style="font-size:10px;color:rgba(255,255,255,0.5);line-height:1.5;margin:0">{subtitulo}</p>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <div style="background:linear-gradient(90deg,{c1},{c2});border-radius:20px;padding:6px 16px;font-size:10px;font-weight:800;color:#fff">{cta}</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.25);font-weight:600">{ig_user}</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">1,984 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_post_tech_futurista(empresa, contenido, estructura) -> str:
    """Fondo oscuro con grid SVG, neon border, headline en 3 bloques visuales."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 8)
    cta = _s(contenido.cta or "Explorar →", 35)
    palabras = titulo.split()
    w1 = " ".join(palabras[:2]) if len(palabras) >= 2 else titulo
    w2 = " ".join(palabras[2:5]) if len(palabras) > 2 else ""
    w3 = " ".join(palabras[5:]) if len(palabras) > 5 else ""
    categoria = _detectar_categoria(contenido, empresa)

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
    <div class="nxar-post-frame" style="background:#020408;position:relative;overflow:hidden;aspect-ratio:1/1">
      <!-- Grid de fondo -->
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.18" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="tf_grid" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
            <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{c1}" stroke-width="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#tf_grid)"/>
      </svg>
      <!-- Glow esquinas -->
      <div style="position:absolute;top:-40px;left:-40px;width:180px;height:180px;background:radial-gradient({c1}30,transparent 65%);border-radius:50%"></div>
      <div style="position:absolute;bottom:-40px;right:-40px;width:180px;height:180px;background:radial-gradient({c2}25,transparent 65%);border-radius:50%"></div>
      <!-- Borde neon -->
      <div style="position:absolute;inset:8px;border:1px solid {c1}55;border-radius:4px;pointer-events:none"></div>
      <!-- Contenido centrado -->
      <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px 20px;text-align:center">
        <div style="font-size:8px;font-weight:700;letter-spacing:0.25em;color:{c1};margin-bottom:18px;text-transform:uppercase">{_s(categoria,20)} · {_s(nombre,14)}</div>
        <div style="font-size:clamp(28px,6vw,38px);font-weight:900;color:#fff;line-height:1.05;letter-spacing:-0.05em;margin:0 0 4px">{w1}</div>
        {f'<div style="font-size:clamp(22px,5vw,30px);font-weight:900;color:{c1};line-height:1.05;letter-spacing:-0.04em;margin:0 0 4px">{w2}</div>' if w2 else ""}
        {f'<div style="font-size:clamp(16px,3.5vw,22px);font-weight:700;color:rgba(255,255,255,0.6);line-height:1.1;letter-spacing:-0.02em;margin:0 0 16px">{w3}</div>' if w3 else '<div style="margin-bottom:16px"></div>'}
        <!-- Línea divisora con gradiente -->
        <div style="width:60px;height:1px;background:linear-gradient(90deg,transparent,{c1},{c2},transparent);margin:0 0 16px"></div>
        <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.7);border:1px solid {c1}88;border-radius:20px;padding:5px 16px">{cta}</div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">2,458 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_post_ia_neural(empresa, contenido, estructura) -> str:
    """Nodos SVG interconectados como fondo + headline IA centrado con gradiente cian-púrpura."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 7)
    copy1 = _s(contenido.copy.split("\n")[0], 80)
    cta = _s(contenido.cta or "Ver demo →", 35)

    # Nodos SVG de red neural (posiciones fijas, colores de marca)
    nodos_svg = f"""
    <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.35" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
      <!-- Conexiones -->
      <line x1="50" y1="80"  x2="140" y2="140" stroke="{c1}" stroke-width="0.8" opacity="0.6"/>
      <line x1="140" y1="140" x2="230" y2="70"  stroke="{c1}" stroke-width="0.8" opacity="0.6"/>
      <line x1="140" y1="140" x2="200" y2="220" stroke="{c2}" stroke-width="0.8" opacity="0.6"/>
      <line x1="80"  y1="220" x2="140" y2="140" stroke="{c2}" stroke-width="0.8" opacity="0.6"/>
      <line x1="230" y1="70"  x2="260" y2="180" stroke="{c1}" stroke-width="0.5" opacity="0.4"/>
      <line x1="260" y1="180" x2="200" y2="220" stroke="{c2}" stroke-width="0.5" opacity="0.4"/>
      <line x1="50"  y1="80"  x2="80"  y2="220" stroke="{c1}" stroke-width="0.4" opacity="0.3"/>
      <!-- Nodos -->
      <circle cx="140" cy="140" r="8"  fill="{c1}" opacity="0.9"/>
      <circle cx="50"  cy="80"  r="5"  fill="{c2}" opacity="0.7"/>
      <circle cx="230" cy="70"  r="5"  fill="{c1}" opacity="0.7"/>
      <circle cx="200" cy="220" r="5"  fill="{c2}" opacity="0.7"/>
      <circle cx="80"  cy="220" r="5"  fill="{c1}" opacity="0.7"/>
      <circle cx="260" cy="180" r="4"  fill="{c2}" opacity="0.5"/>
      <circle cx="140" cy="140" r="14" fill="{c1}" opacity="0.15"/>
    </svg>"""

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
    <div class="nxar-post-frame" style="background:linear-gradient(150deg,#030810,#080412);position:relative;overflow:hidden;aspect-ratio:1/1">
      {nodos_svg}
      <!-- Overlay central -->
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 30%,#030810 80%)"></div>
      <!-- Contenido -->
      <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center">
        <!-- Badge IA -->
        <div style="font-size:7px;font-weight:900;letter-spacing:0.25em;color:{c1};background:{c1}18;border:1px solid {c1}44;border-radius:3px;padding:3px 10px;margin-bottom:14px">◈ INTELIGENCIA ARTIFICIAL</div>
        <!-- Headline con gradiente -->
        <h2 style="font-size:{_afs(titulo,'post')};font-weight:900;line-height:1.1;letter-spacing:-0.04em;margin:0 0 10px;background:linear-gradient(135deg,#fff 30%,{c1},{c2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{titulo}</h2>
        <p style="font-size:10px;color:rgba(255,255,255,0.45);line-height:1.5;margin:0 0 18px;max-width:200px">{copy1}</p>
        <!-- Línea divisora -->
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
          <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,{c1}66)"></div>
          <div style="font-size:14px;color:{c1};opacity:0.6">◈</div>
          <div style="flex:1;height:1px;background:linear-gradient(90deg,{c2}66,transparent)"></div>
        </div>
        <div style="background:linear-gradient(90deg,{c1},{c2});border-radius:20px;padding:6px 18px;font-size:10px;font-weight:800;color:#fff">{cta}</div>
        <div style="margin-top:12px;font-size:8px;color:rgba(255,255,255,0.2)">{_s(nombre,16)}</div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">2,103 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_post_dashboard_analytics(empresa, contenido, estructura) -> str:
    """Mockup de dashboard oscuro con 4 KPI tiles y sparkline SVG simulado."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 8)
    cta = _s(contenido.cta or "Ver reporte →", 35)
    categoria = _detectar_categoria(contenido, empresa)

    _kpi_data = {
        "ia":            [("98%","Precisión","↑"),("4.2x","ROI","↑"),("73%","Tiempo ↓","↓"),("2.1k","Usuarios","↑")],
        "software":      [("99.9%","Uptime","↑"),("0.3s","Latencia","↓"),("14k","Req/min","↑"),("4.8★","Rating","↑")],
        "marketing":     [("6.8%","CTR","↑"),("2.4x","ROAS","↑"),("12k","Leads","↑"),("$18","CPA","↓")],
        "automatizacion":[("87%","Ahorro","↑"),("5x","Velocidad","↑"),("0 err","Errores","✓"),("24/7","Operación","↑")],
        "finanzas":      [("32%","Margen","↑"),("1.8x","Retorno","↑"),("$2.4M","Revenue","↑"),("A+","Rating","↑")],
    }
    kpis = _kpi_data.get(categoria, [("87%","Resultado","↑"),("3.2x","Crecimiento","↑"),("98%","Satisfacción","↑"),("4.9★","Valoración","↑")])

    def kpi_tile(val, lbl, trend):
        trend_col = "#10b981" if trend in ("↑","✓") else "#ef4444"
        return (f'<div style="flex:1;background:#0e1628;border:1px solid rgba(255,255,255,0.07);border-radius:6px;padding:8px 6px;text-align:center">'
                f'<div style="font-size:14px;font-weight:900;color:#fff;line-height:1">{val}</div>'
                f'<div style="font-size:7px;color:rgba(255,255,255,0.4);margin:2px 0">{lbl}</div>'
                f'<div style="font-size:8px;font-weight:700;color:{trend_col}">{trend}</div>'
                f'</div>')

    tiles_html = "".join(kpi_tile(*k) for k in kpis)

    # Sparkline SVG simple (línea de tendencia ascendente)
    sparkline = f"""<svg viewBox="0 0 120 30" style="width:100%;height:30px" xmlns="http://www.w3.org/2000/svg">
      <polyline points="0,25 20,20 40,18 60,14 80,10 100,6 120,2" fill="none" stroke="{c1}" stroke-width="1.5"/>
      <polyline points="0,25 20,20 40,18 60,14 80,10 100,6 120,2 120,30 0,30" fill="{c1}" opacity="0.08"/>
    </svg>"""

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
    <div class="nxar-post-frame" style="background:#060d1a;position:relative;overflow:hidden;aspect-ratio:1/1;display:flex;flex-direction:column;padding:16px">
      <!-- Header del dashboard -->
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
        <div>
          <div style="font-size:8px;font-weight:700;letter-spacing:0.12em;color:rgba(255,255,255,0.35);margin-bottom:2px">ANALYTICS · {_s(categoria.upper(),16)}</div>
          <div style="font-size:13px;font-weight:800;color:#fff;letter-spacing:-0.02em">{_s(nombre,18)}</div>
        </div>
        <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,{c1},{c2});display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:13px">{initial}</div>
      </div>
      <!-- KPI tiles -->
      <div style="display:flex;gap:6px;margin-bottom:12px">{tiles_html}</div>
      <!-- Gráfica de tendencia -->
      <div style="background:#0e1628;border:1px solid rgba(255,255,255,0.07);border-radius:6px;padding:8px 10px;flex:1;display:flex;flex-direction:column;justify-content:space-between">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
          <div style="font-size:8px;font-weight:600;color:rgba(255,255,255,0.4)">Tendencia — últimas semanas</div>
          <div style="font-size:7px;color:{c1};font-weight:700">↑ Creciendo</div>
        </div>
        {sparkline}
      </div>
      <!-- CTA -->
      <div style="margin-top:10px;display:flex;align-items:center;justify-content:space-between">
        <h3 style="font-size:11px;font-weight:700;color:#fff;line-height:1.2;margin:0;max-width:65%">{titulo}</h3>
        <div style="background:linear-gradient(90deg,{c1},{c2});border-radius:16px;padding:5px 12px;font-size:9px;font-weight:800;color:#fff;white-space:nowrap">{cta}</div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">1,672 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_post_modern_gradient(empresa, contenido, estructura) -> str:
    """Gradiente diagonal vibrante de pantalla completa, texto en capas, patrón de puntos."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _tw(contenido.titulo, 8)
    copy1 = _s(contenido.copy.split("\n")[0], 80)
    cta = _s(contenido.cta or "Saber más →", 35)
    secciones = estructura.get("secciones", [])
    beneficio = next((s["texto"] for s in secciones if s.get("tipo") == "beneficio"), copy1)

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
    <div class="nxar-post-frame" style="background:linear-gradient(135deg,{c1} 0%,{c2} 55%,#1a0a2e 100%);position:relative;overflow:hidden;aspect-ratio:1/1">
      <!-- Patrón de puntos superpuesto -->
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.1" xmlns="http://www.w3.org/2000/svg">
        <defs><pattern id="mg_dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
          <circle cx="1.5" cy="1.5" r="1.5" fill="#fff"/>
        </pattern></defs>
        <rect width="100%" height="100%" fill="url(#mg_dots)"/>
      </svg>
      <!-- Círculos de fondo decorativos -->
      <div style="position:absolute;top:-30px;right:-30px;width:160px;height:160px;border:40px solid rgba(255,255,255,0.06);border-radius:50%"></div>
      <div style="position:absolute;bottom:-50px;left:-50px;width:200px;height:200px;border:50px solid rgba(255,255,255,0.04);border-radius:50%"></div>
      <!-- Contenido -->
      <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:22px 20px">
        <!-- Top row -->
        <div style="display:flex;align-items:center;justify-content:space-between">
          <div style="font-size:9px;font-weight:800;color:rgba(255,255,255,0.9);letter-spacing:0.06em">{_s(nombre,16)}</div>
          <div style="width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.15);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,0.3);display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:13px">{initial}</div>
        </div>
        <!-- Headline central -->
        <div style="text-align:center">
          <h2 style="font-size:{_afs(titulo,'post')};font-weight:900;color:#fff;line-height:1.1;letter-spacing:-0.04em;margin:0 0 10px;text-shadow:0 2px 12px rgba(0,0,0,0.3)">{titulo}</h2>
          <p style="font-size:11px;color:rgba(255,255,255,0.75);line-height:1.5;margin:0 auto;max-width:210px">{_s(beneficio,75)}</p>
        </div>
        <!-- CTA bottom -->
        <div style="display:flex;align-items:center;justify-content:center">
          <div style="background:rgba(255,255,255,0.95);border-radius:24px;padding:8px 22px;font-size:10px;font-weight:900;color:{c1};box-shadow:0 4px 20px rgba(0,0,0,0.25)">{cta}</div>
        </div>
      </div>
    </div>
    <div class="nxar-ig-footer">
      <div class="nxar-ig-actions">
        <span class="nxar-ig-action">♡</span><span class="nxar-ig-action">💬</span>
        <span class="nxar-ig-action">↗</span><span class="nxar-ig-action nxar-ig-action--right">🔖</span>
      </div>
      <div class="nxar-ig-likes">3,047 Me gusta</div>
      <div class="nxar-ig-caption"><b>{ig_user}</b> {titulo[:55]}...</div>
    </div>
  </div>
</div>"""


def _render_historia(empresa, contenido, estructura, estilo=None) -> str:
    """Dispatcher hacia 5 renderers distintos por estilo de historia."""
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    pantallas = estructura.get("pantallas", [])
    estilo_id = (estilo or {}).get("id", "encuesta")

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)
    vpack = get_visual_pack(categoria, c1, c2)

    # ── Fondos por estilo (colores dominantes muy distintos entre sí) ──────────
    _bgs = {
        "encuesta":       [f"linear-gradient(145deg,{c1},{c2})", f"linear-gradient(160deg,{c2}bb,#0f172a)", "#0f172a"],
        "quiz":           ["linear-gradient(145deg,#1a0a2e,#0d0828)", "linear-gradient(160deg,#100d1e,#0a0818)", f"linear-gradient(145deg,#0f0a2e,{c1}33)"],
        "antes_despues":  ["linear-gradient(145deg,#2d0a0a,#1a0505)", "linear-gradient(160deg,#1a1a2e,#0f172a)", f"linear-gradient(145deg,{c1},{c2})"],
        "cta_urgente":    ["linear-gradient(145deg,#0a0a0a,#111118)", f"linear-gradient(160deg,{c1}33,{c2}22)", f"linear-gradient(145deg,{c1},{c2})"],
        "detras_camaras": ["linear-gradient(145deg,#2a1500,#1a0d00)", "linear-gradient(160deg,#231200,#2a1a05)", f"linear-gradient(145deg,{c1}cc,#3a1500)"],
    }
    bg_pantallas = _bgs.get(estilo_id, _bgs["encuesta"])

    def _body_content(i: int, p: dict) -> str:
        titulo = _s(p.get("titulo", ""), 80)
        sub = _s(p.get("subtitulo", ""), 60)
        sub_html = f'<p class="nxar-story-sub">{sub}</p>' if sub else ""
        fs = _afs(titulo, "story")

        # ── ENCUESTA ─────────────────────────────────────────────────────────
        if estilo_id == "encuesta":
            if i == 0:
                return (
                    f'<div style="flex:0 0 38%;overflow:hidden;border-radius:8px;margin-bottom:8px;position:relative">{vpack["hero"]}</div>'
                    f'<p class="nxar-story-titulo" style="text-align:center;font-size:{fs}">{titulo}</p>'
                    f'<div class="nxar-sticker nxar-sticker--encuesta"><span>¿Qué opinas?</span>'
                    f'<div class="nxar-encuesta-op" style="border-color:{c1};background:{c1}22">Sí 👍</div>'
                    f'<div class="nxar-encuesta-op">No 👎</div></div>'
                )
            if i == 1:
                return (
                    f'<div style="width:85%;background:rgba(255,255,255,0.1);border-radius:4px;height:4px;margin:0 auto 10px">'
                    f'<div style="width:55%;height:100%;background:{c1};border-radius:4px"></div></div>'
                    f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
                    f'<div class="nxar-sticker nxar-sticker--deslizador">Reacciona 😍'
                    f'<div class="nxar-deslizador-track"><div class="nxar-deslizador-thumb" style="background:{c1}">😍</div></div></div>'
                )
            return (
                f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
                f'<div style="background:linear-gradient(90deg,{c1},{c2});border-radius:24px;padding:10px 22px;'
                f'font-size:12px;font-weight:800;color:#fff;display:inline-block;margin:8px auto 0;'
                f'box-shadow:0 4px 14px {c1}44">Ver más →</div>'
                f'<div class="nxar-sticker nxar-sticker--link" style="border-color:{c1};color:{c1};margin:6px auto 0">🔗 Ver más</div>'
            )

        # ── QUIZ ─────────────────────────────────────────────────────────────
        if estilo_id == "quiz":
            if i == 0:
                return (
                    f'<div style="font-size:56px;text-align:center;margin-bottom:4px;line-height:1">❓</div>'
                    f'<div style="font-size:8px;font-weight:800;letter-spacing:0.2em;color:rgba(255,255,255,0.35);'
                    f'text-align:center;margin-bottom:8px">TRIVIA · ¿LO SABÍAS?</div>'
                    f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
                )
            if i == 1:
                op_a = titulo[:24] + "..." if len(titulo) > 24 else titulo
                op_b = sub[:24] if sub else "Opción correcta"
                return (
                    f'<div style="font-size:8px;font-weight:700;color:rgba(255,255,255,0.35);'
                    f'letter-spacing:0.1em;margin-bottom:8px;text-align:center">SELECCIONA TU RESPUESTA</div>'
                    f'<div style="display:flex;flex-direction:column;gap:6px;width:100%">'
                    f'<div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);'
                    f'border-radius:8px;padding:7px 12px;font-size:10px;color:rgba(255,255,255,0.6)">A · {op_a}</div>'
                    f'<div style="background:{c1}22;border:1px solid {c1}55;border-radius:8px;'
                    f'padding:7px 12px;font-size:10px;color:{c1};font-weight:700">B · {op_b} ✓</div>'
                    f'<div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);'
                    f'border-radius:8px;padding:7px 12px;font-size:10px;color:rgba(255,255,255,0.6)">C · Ver más</div>'
                    f'</div>'
                )
            return (
                f'<div style="background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);'
                f'border-radius:10px;padding:10px 14px;margin-bottom:8px;width:100%">'
                f'<div style="font-size:8px;font-weight:800;color:#22c55e;letter-spacing:0.12em;margin-bottom:4px">✓ RESPUESTA CORRECTA</div>'
                f'<p style="font-size:11px;color:#fff;margin:0">{titulo}</p></div>'
                f'{sub_html}<div class="nxar-sticker nxar-sticker--link" style="border-color:{c1};color:{c1}">🔗 Más curiosidades</div>'
            )

        # ── ANTES / DESPUÉS ───────────────────────────────────────────────────
        if estilo_id == "antes_despues":
            if i == 0:
                return (
                    f'<div style="font-size:9px;font-weight:900;letter-spacing:0.2em;color:#ef4444;'
                    f'background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.4);'
                    f'border-radius:6px;padding:5px 14px;display:inline-block;margin-bottom:10px">📌 ANTES</div>'
                    f'<div style="font-size:42px;text-align:center;margin-bottom:6px">😰</div>'
                    f'<p class="nxar-story-titulo" style="text-align:center;color:#fca5a5;font-size:{fs}">{titulo}</p>{sub_html}'
                )
            if i == 1:
                return (
                    f'<div style="font-size:8px;font-weight:700;color:rgba(255,255,255,0.4);'
                    f'letter-spacing:0.12em;text-align:center;margin-bottom:10px">↕ COMPARANDO...</div>'
                    f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
                    f'<div style="display:flex;gap:8px;justify-content:center;margin-top:8px">'
                    f'<div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);'
                    f'border-radius:6px;padding:6px 10px;font-size:9px;color:#fca5a5;flex:1;text-align:center">ANTES ❌</div>'
                    f'<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);'
                    f'border-radius:6px;padding:6px 10px;font-size:9px;color:#86efac;flex:1;text-align:center">DESPUÉS ✓</div>'
                    f'</div>'
                )
            return (
                f'<div style="font-size:9px;font-weight:900;letter-spacing:0.2em;color:#22c55e;'
                f'background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.35);'
                f'border-radius:6px;padding:5px 14px;display:inline-block;margin-bottom:10px">✨ DESPUÉS</div>'
                f'<div style="font-size:42px;text-align:center;margin-bottom:6px">🎯</div>'
                f'<p class="nxar-story-titulo" style="text-align:center;color:#86efac;font-size:{fs}">{titulo}</p>{sub_html}'
                f'<div style="background:linear-gradient(90deg,#22c55e,{c1});border-radius:24px;'
                f'padding:9px 20px;font-size:11px;font-weight:800;color:#fff;display:inline-block;margin-top:8px">'
                f'Quiero este resultado →</div>'
            )

        # ── CTA URGENTE ───────────────────────────────────────────────────────
        if estilo_id == "cta_urgente":
            if i == 0:
                digits_html = "".join(
                    f'<div style="background:{c1};border-radius:4px;min-width:22px;height:32px;'
                    f'display:flex;align-items:center;justify-content:center;'
                    f'font-size:11px;font-weight:900;color:#fff;{"margin:0 2px" if d in (":",) else ""}">{d}</div>'
                    for d in ["0", "8", ":", "0", "0"]
                )
                return (
                    f'<div style="font-size:9px;font-weight:900;letter-spacing:0.15em;color:#fbbf24;'
                    f'background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.35);'
                    f'border-radius:6px;padding:5px 12px;display:inline-block;margin-bottom:8px">⚡ OFERTA LIMITADA</div>'
                    f'<p class="nxar-story-titulo" style="text-align:center;font-size:{fs}">{titulo}</p>'
                    f'<div style="display:flex;align-items:center;justify-content:center;gap:2px;margin-top:8px">{digits_html}</div>'
                    f'<div style="font-size:8px;color:rgba(255,255,255,0.3);margin-top:4px;text-align:center">HH : MM</div>'
                )
            if i == 1:
                bens = [titulo[:28], sub[:28] if sub else "Acceso inmediato", "Sin permanencia"]
                items_html = "".join(
                    f'<div style="display:flex;align-items:center;gap:6px;font-size:10px;color:#fff;margin-bottom:5px">'
                    f'<span style="color:#22c55e;font-size:13px;flex-shrink:0">✓</span>{b}</div>'
                    for b in bens
                )
                return (
                    f'<div style="font-size:8px;font-weight:800;letter-spacing:0.1em;color:{c1};margin-bottom:8px">¿QUÉ INCLUYE?</div>'
                    f'{items_html}'
                    f'<div style="margin-top:8px;font-size:8px;font-weight:700;color:rgba(255,255,255,0.3);'
                    f'letter-spacing:0.08em">🔒 ACCESO LIMITADO</div>'
                )
            return (
                f'<p class="nxar-story-titulo" style="text-align:center;font-size:{fs}">{titulo}</p>'
                f'<div style="background:linear-gradient(90deg,{c1},{c2});border-radius:24px;'
                f'padding:12px 26px;font-size:13px;font-weight:900;color:#fff;display:inline-block;'
                f'margin:10px auto 0;box-shadow:0 6px 20px {c1}55;letter-spacing:0.04em">ACCESO AHORA →</div>'
                f'<div style="font-size:8px;color:rgba(255,255,255,0.3);margin-top:6px;text-align:center">Solo quedan pocas plazas</div>'
            )

        # ── DETRÁS DE CÁMARAS ────────────────────────────────────────────────
        # (también es el fallback para estilos desconocidos)
        if i == 0:
            return (
                f'<div style="font-size:8px;font-weight:700;color:#f59e0b;letter-spacing:0.15em;'
                f'text-align:center;margin-bottom:6px">📸 DETRÁS DE CÁMARAS</div>'
                f'<div style="font-size:52px;text-align:center;margin-bottom:6px;opacity:0.25">📷</div>'
                f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
            )
        if i == 1:
            steps = ["Planificamos", "Ejecutamos", "Medimos resultados"]
            steps_html = "".join(
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">'
                f'<div style="background:{c1};width:18px;height:18px;border-radius:50%;flex-shrink:0;'
                f'display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#fff">{j+1}</div>'
                f'<span style="font-size:10px;color:rgba(255,255,255,0.75)">{s}</span></div>'
                for j, s in enumerate(steps)
            )
            return (
                f'<div style="font-size:8px;font-weight:700;color:#f59e0b;letter-spacing:0.1em;margin-bottom:10px">🛠 ASÍ LO HACEMOS</div>'
                f'{steps_html}'
                f'<p style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:6px">{titulo}</p>'
            )
        return (
            f'<div style="font-size:8px;font-weight:700;color:#f59e0b;text-align:center;margin-bottom:6px">ESTE ES NUESTRO TRABAJO</div>'
            f'<p class="nxar-story-titulo" style="text-align:center">{titulo}</p>{sub_html}'
            f'<div class="nxar-sticker nxar-sticker--link" style="border-color:{c1};color:{c1};margin-top:8px">🔗 Conoce el equipo</div>'
        )

    screens_html = ""
    total = max(len(pantallas), 3)
    for i, p in enumerate(pantallas[:3]):
        bg = bg_pantallas[i] if i < len(bg_pantallas) else bg_pantallas[-1]
        dur = p.get("duracion", "7s")
        bars = "".join(
            f'<div class="nxar-story-bar '
            f'{"nxar-story-bar--done" if j < i else "nxar-story-bar--active" if j == i else ""}"></div>'
            for j in range(total)
        )
        body = _body_content(i, p)
        screens_html += f"""
    <div class="nxar-story-screen" style="background:{bg}">
      {vis['pattern'] if i == 0 else ""}
      <div class="nxar-story-bars">{bars}</div>
      <div class="nxar-story-account">
        <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
        <span class="nxar-story-username">{_s(nombre, 20)}</span>
        <span class="nxar-story-time">{dur}</span>
        <span class="nxar-story-x">✕</span>
      </div>
      <div class="nxar-story-body" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
        {body}
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


def _render_carrusel(empresa, contenido, estructura, estilo=None) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    slides = estructura.get("slides", [])
    total = len(slides)

    categoria = _detectar_categoria(contenido, empresa)
    vis = _bloque_visual(categoria, c1, c2)
    vpack = get_visual_pack(categoria, c1, c2)
    accents = vis["slide_accent"]

    tipo_bg = {
        "portada":     f"linear-gradient(145deg,{c1},{c2})",
        "problema":    "linear-gradient(145deg,#1e1028,#16213e)",
        "consecuencia":"linear-gradient(145deg,#2a1018,#1a0d14)",
        "contenido":   "linear-gradient(145deg,#0d1b2e,#16213e)",
        "solucion":    f"linear-gradient(145deg,#0d2137,#0a2040)",
        "beneficio":   "linear-gradient(145deg,#0d2137,#0a1628)",
        "cierre":      "linear-gradient(145deg,#12203a,#0d1b2e)",
        "cta":         f"linear-gradient(145deg,{c2},{c1})",
    }
    tipo_icon = {
        "portada": vis["icon"], "problema": "⚡", "consecuencia": "⚠",
        "contenido": "◈", "solucion": "✓", "beneficio": "✓", "cierre": "→", "cta": "★",
    }

    estilo_id = (estilo or {}).get("id", "problema_solucion")

    # Etiquetas y decoraciones por estilo de carrusel
    _caso_labels = ["PORTADA", "CLIENTE", "DESAFÍO", "PROCESO", "RESULTADO", "CTA"]
    _tutorial_labels = ["PORTADA", "PASO 01", "PASO 02", "PASO 03", "PASO 04", "CTA"]

    def _estilo_slide_extra(slide_idx: int, slide_tipo: str) -> str:
        if estilo_id == "lista_numerada" and slide_idx > 0 and slide_tipo not in ("cta", "portada"):
            num_str = str(slide_idx).zfill(2)
            return (
                f'<div style="position:absolute;top:12px;right:14px;font-size:48px;font-weight:900;'
                f'color:{c1};opacity:0.12;line-height:1;letter-spacing:-0.04em">{num_str}</div>'
                f'<div style="font-size:9px;font-weight:700;color:{c1};letter-spacing:0.15em;margin-bottom:4px"># {num_str}</div>'
            )
        if estilo_id == "tutorial_pasos" and slide_idx > 0 and slide_tipo not in ("cta",):
            label = _tutorial_labels[slide_idx] if slide_idx < len(_tutorial_labels) else f"PASO {slide_idx:02d}"
            return (
                f'<div style="font-size:9px;font-weight:800;letter-spacing:0.15em;color:#f97316;'
                f'background:rgba(249,115,22,0.12);border:1px solid rgba(249,115,22,0.35);border-radius:4px;padding:3px 9px;'
                f'display:inline-block;margin-bottom:6px">{label}</div>'
            )
        if estilo_id == "caso_exito" and slide_idx < len(_caso_labels):
            label = _caso_labels[slide_idx]
            color_map = {"PORTADA": c1, "CLIENTE": "#8b5cf6", "DESAFÍO": "#ef4444", "PROCESO": "#f59e0b", "RESULTADO": "#22c55e", "CTA": c2}
            col = color_map.get(label, "#8b5cf6")
            return (
                f'<div style="font-size:9px;font-weight:800;letter-spacing:0.12em;'
                f'color:{col};background:{col}18;border:1px solid {col}44;'
                f'border-radius:4px;padding:3px 8px;display:inline-block;margin-bottom:5px">{label}</div>'
            )
        if estilo_id == "mitos_realidad" and slide_idx > 0 and slide_tipo not in ("cta",):
            is_mito = slide_idx % 2 != 0
            if is_mito:
                return '<div style="font-size:9px;font-weight:800;letter-spacing:0.12em;color:#ef4444;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);border-radius:4px;padding:3px 8px;display:inline-block;margin-bottom:5px">❌ MITO</div>'
            else:
                return f'<div style="font-size:9px;font-weight:800;letter-spacing:0.12em;color:#22c55e;background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);border-radius:4px;padding:3px 8px;display:inline-block;margin-bottom:5px">✓ REALIDAD</div>'
        return ""

    def _estilo_slide_bg(slide_idx: int, slide_tipo: str, default_bg: str) -> str:
        if slide_tipo in ("portada", "cta"):
            return default_bg
        if estilo_id == "mitos_realidad" and slide_idx > 0:
            is_mito = slide_idx % 2 != 0
            return "linear-gradient(145deg,#2d0a0a,#1a0505)" if is_mito else "linear-gradient(145deg,#0a2d0a,#051a05)"
        if estilo_id == "lista_numerada":
            return "linear-gradient(145deg,#0a1528,#081020)"
        if estilo_id == "tutorial_pasos":
            return "linear-gradient(145deg,#1a0e00,#100a00)"
        if estilo_id == "caso_exito":
            return "linear-gradient(145deg,#120a2e,#0c0820)"
        return default_bg

    slides_html = ""
    for i, s in enumerate(slides):
        tipo = s.get("tipo", "contenido")
        bg_default = tipo_bg.get(tipo, "linear-gradient(145deg,#1a1a2e,#0f172a)")
        bg = _estilo_slide_bg(i, tipo, bg_default)
        icon = tipo_icon.get(tipo, vis["icon"])
        active = "nxar-slide--active" if i == 0 else ""
        accent_html = accents.get(tipo, "")
        estilo_extra = _estilo_slide_extra(i, tipo)

        pattern_html = vis["pattern"] if tipo in ("portada", "cta") else _pattern_grid()

        if tipo == "portada":
            # Zona visual grande (45%) + zona texto (55%) — igual al layout del post
            hero_zone = (
                f'<div style="height:45%;position:relative;overflow:hidden;background:linear-gradient(160deg,#06080f,#080c18)">'
                f'{vpack["hero"]}'
                f'<div style="position:absolute;inset:0;background:linear-gradient(transparent 65%,{bg_default})"></div>'
                f'<div style="position:absolute;top:8px;left:10px;font-size:7px;font-weight:700;letter-spacing:0.12em;color:{c1};background:{c1}18;border:1px solid {c1}44;border-radius:3px;padding:2px 6px">{_s(categoria.upper(),16)}</div>'
                f'<div style="position:absolute;top:8px;right:10px;font-size:8px;font-weight:700;color:rgba(255,255,255,0.6);background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:2px 7px">{_s(nombre,12)}</div>'
                f'</div>'
            )
            slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};display:flex;flex-direction:column;overflow:hidden">
      {hero_zone}
      <div class="nxar-slide-content" style="flex:1;display:flex;flex-direction:column;justify-content:space-between;padding:10px 14px">
        <div>
          <div style="width:24px;height:2px;background:linear-gradient(90deg,{c1},{c2});border-radius:1px;margin-bottom:6px"></div>
          <h2 class="nxar-slide-titulo" style="font-size:{_afs(_s(s.get('titulo',''),80),'slide')};margin:0 0 4px">{_s(s.get('titulo', ''), 80)}</h2>
          {f'<p class="nxar-slide-sub" style="font-size:10px;opacity:0.55;margin:0">{_s(s.get("subtitulo",""),60)}</p>' if s.get("subtitulo") else ''}
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div style="font-size:7px;font-weight:700;color:{c1};letter-spacing:0.1em">{vis["icon"]} {vis["label"]}</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.3)">{i+1}/{total} ›</div>
        </div>
        {_slide_body(tipo, s, vis, c1, c2)}
      </div>
    </div>"""
        else:
            # Variables pre-computadas para evitar expresiones complejas en f-strings (Python 3.11)
            tit = _s(s.get("titulo", ""), 80)
            sub_txt = _s(s.get("subtitulo", ""), 70)
            sub_p = f'<p class="nxar-slide-sub" style="margin:4px 0 0">{sub_txt}</p>' if sub_txt else ""
            sub_p_center = f'<p class="nxar-slide-sub" style="text-align:center;margin:4px 0 0">{sub_txt}</p>' if sub_txt else ""
            sub_p_muted = f'<p class="nxar-slide-sub" style="margin:0;font-size:10px;color:rgba(255,255,255,0.6)">{sub_txt}</p>' if sub_txt else ""
            sub_p_default = f'<p class="nxar-slide-sub">{sub_txt}</p>' if sub_txt else ""
            logo_html = f'<div class="nxar-slide-logo" style="color:rgba(255,255,255,0.25)">{_s(nombre, 14)}</div>' if i == total - 1 else ""
            is_cta = tipo in ("cta", "cierre")
            tpl_marker = (
                f'<div style="position:absolute;bottom:3px;left:50%;transform:translateX(-50%);'
                f'font-size:7px;font-weight:700;color:rgba(255,255,255,0.35);background:rgba(0,0,0,0.55);'
                f'border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:2px 8px;'
                f'white-space:nowrap;z-index:10;letter-spacing:0.08em">TEMPLATE: {estilo_id}</div>'
            )

            # ── LISTA NUMERADA: layout magazine — número gigante izquierda + contenido derecha ──
            if estilo_id == "lista_numerada" and not is_cta:
                num_str = str(i).zfill(2)
                lbl = vis["label"][:14]
                slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};position:relative;overflow:hidden">
      {pattern_html}
      <div class="nxar-slide-content" style="display:flex;flex-direction:column;padding:12px 14px;height:100%">
        <div style="display:flex;align-items:stretch;gap:10px;flex:1;min-height:0">
          <div style="width:48px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative">
            <div style="font-size:58px;font-weight:900;color:{c1};opacity:0.14;line-height:1;position:absolute;top:50%;transform:translateY(-50%)">{num_str}</div>
            <div style="font-size:8px;font-weight:700;color:{c1};letter-spacing:0.15em;writing-mode:vertical-rl;transform:rotate(180deg)"># {num_str}</div>
          </div>
          <div style="flex:1;border-left:2px solid {c1}44;padding-left:10px;display:flex;flex-direction:column;justify-content:center;gap:6px;overflow:hidden">
            <div style="font-size:7px;font-weight:700;color:rgba(255,255,255,0.3);letter-spacing:0.12em">{tipo.upper()}</div>
            <h2 class="nxar-slide-titulo" style="font-size:{_afs(tit,'slide')};margin:0">{tit}</h2>
            {sub_p}
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.08)">
          <div style="font-size:7px;font-weight:700;color:{c1};letter-spacing:0.1em">TOP {total - 2} · {lbl}</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.3)">{i + 1}/{total}</div>
        </div>
      </div>
      {tpl_marker}
    </div>"""

            # ── MITOS VS REALIDAD: veredicto centrado — ❌ MITO / ✅ REALIDAD dominante ──
            elif estilo_id == "mitos_realidad" and not is_cta:
                is_mito = i % 2 != 0
                v_icon = "❌" if is_mito else "✅"
                v_text = "MITO" if is_mito else "REALIDAD"
                v_color = "#ef4444" if is_mito else "#22c55e"
                dots_mr = "".join(
                    f'<div style="width:14px;height:3px;border-radius:2px;background:rgba(255,255,255,{0.7 if j == i else 0.2})"></div>'
                    for j in range(min(total, 8))
                )
                slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};position:relative;overflow:hidden">
      {pattern_html}
      <div class="nxar-slide-content" style="display:flex;flex-direction:column;align-items:center;text-align:center;padding:10px 14px;height:100%;justify-content:space-between">
        <div style="display:flex;justify-content:space-between;width:100%;align-items:center">
          <div style="font-size:8px;font-weight:700;color:rgba(255,255,255,0.3);letter-spacing:0.1em">{tipo.upper()}</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.3)">{i + 1}/{total}</div>
        </div>
        <div style="text-align:center;padding:6px 0">
          <div style="font-size:50px;line-height:1;margin-bottom:6px">{v_icon}</div>
          <div style="font-size:11px;font-weight:900;color:{v_color};letter-spacing:0.2em;background:{v_color}1a;border:1px solid {v_color}44;border-radius:6px;padding:4px 14px;display:inline-block">{v_text}</div>
        </div>
        <div style="overflow:hidden;max-width:100%">
          <h2 class="nxar-slide-titulo" style="font-size:{_afs(tit,'slide')};text-align:center;margin:0">{tit}</h2>
          {sub_p_center}
        </div>
        <div style="display:flex;gap:3px;align-items:center">{dots_mr}</div>
      </div>
      {tpl_marker}
    </div>"""

            # ── CASO DE ÉXITO: fases en timeline superior + tarjeta de contenido ──
            elif estilo_id == "caso_exito" and not is_cta:
                phase_idx = min(i, len(_caso_labels) - 1)
                phase_label = _caso_labels[phase_idx]
                _ce_colors = {
                    "PORTADA": c1, "CLIENTE": "#8b5cf6",
                    "DESAFÍO": "#ef4444", "PROCESO": "#f59e0b",
                    "RESULTADO": "#22c55e", "CTA": c2,
                }
                active_col = _ce_colors.get(phase_label, "#8b5cf6")
                phases_html = ""
                for pl in [p for p in _caso_labels if p not in ("PORTADA", "CTA")]:
                    ph_c = _ce_colors.get(pl, "#8b5cf6")
                    is_ph = pl == phase_label
                    ph_bg = ph_c + "28" if is_ph else "transparent"
                    ph_bd = ph_c + "55" if is_ph else ph_c + "20"
                    ph_tx = ph_c if is_ph else "rgba(255,255,255,0.2)"
                    phases_html += (
                        f'<div style="font-size:7px;font-weight:700;padding:2px 7px;'
                        f'border-radius:10px;letter-spacing:0.06em;background:{ph_bg};'
                        f'color:{ph_tx};border:1px solid {ph_bd}">{pl}</div>'
                    )
                slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};position:relative;overflow:hidden">
      {pattern_html}
      <div class="nxar-slide-content" style="display:flex;flex-direction:column;padding:10px 12px;height:100%">
        <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px;padding-bottom:7px;border-bottom:1px solid rgba(255,255,255,0.08)">{phases_html}</div>
        <div style="background:{active_col}12;border:1px solid {active_col}33;border-radius:8px;padding:8px 10px;flex:1;display:flex;flex-direction:column;justify-content:center;gap:6px;overflow:hidden">
          <div style="font-size:9px;font-weight:800;color:{active_col};letter-spacing:0.12em">{phase_label}</div>
          <h2 class="nxar-slide-titulo" style="font-size:{_afs(tit,'slide')};margin:0;color:#fff">{tit}</h2>
          {sub_p_muted}
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
          <div style="font-size:7px;font-weight:700;color:{active_col};letter-spacing:0.1em">{vis["icon"]} CASO REAL</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.3)">{i + 1}/{total}</div>
        </div>
      </div>
      {tpl_marker}
    </div>"""

            # ── TUTORIAL PASO A PASO: barra de progreso + número de paso grande ──
            elif estilo_id == "tutorial_pasos" and not is_cta:
                step_label = _tutorial_labels[i] if i < len(_tutorial_labels) else f"PASO {i:02d}"
                progress_pct = int((i / max(total - 1, 1)) * 100)
                num_big = str(max(i, 1)).zfill(2)
                lbl_t = vis["label"][:14]
                slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};position:relative;overflow:hidden">
      {pattern_html}
      <div class="nxar-slide-content" style="display:flex;flex-direction:column;padding:10px 14px;height:100%">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
          <div style="font-size:9px;font-weight:800;letter-spacing:0.15em;color:#f97316;background:rgba(249,115,22,0.12);border:1px solid rgba(249,115,22,0.35);border-radius:4px;padding:3px 9px">{step_label}</div>
          <div style="font-size:8px;color:rgba(255,255,255,0.3)">{i + 1}/{total}</div>
        </div>
        <div style="width:100%;height:3px;background:rgba(255,255,255,0.08);border-radius:2px;margin-bottom:8px;overflow:hidden">
          <div style="height:100%;width:{progress_pct}%;background:linear-gradient(90deg,#f97316,#ea580c);border-radius:2px"></div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:8px;flex:1;overflow:hidden">
          <div style="font-size:46px;font-weight:900;color:#f97316;opacity:0.2;line-height:1;flex-shrink:0;min-width:36px">{num_big}</div>
          <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:4px;overflow:hidden">
            <h2 class="nxar-slide-titulo" style="font-size:{_afs(tit,'slide')};margin:0">{tit}</h2>
            {sub_p}
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.08)">
          <div style="font-size:7px;font-weight:700;color:#f97316;letter-spacing:0.1em">TUTORIAL · {lbl_t}</div>
          <div style="font-size:7px;color:rgba(255,255,255,0.3)">{progress_pct}% COMPLETADO</div>
        </div>
      </div>
      {tpl_marker}
    </div>"""

            else:
                # ── PROBLEMA → SOLUCIÓN (default) + slides CTA de todos los estilos ──
                tpl_m = tpl_marker if not is_cta else ""
                slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg};position:relative">
      {pattern_html}
      <div class="nxar-geo nxar-geo--circle1" style="background:rgba(255,255,255,0.04)"></div>
      {accent_html}
      <div class="nxar-slide-content">
        <div class="nxar-slide-header">
          <div class="nxar-slide-tipo-badge">{tipo.upper()}</div>
          <div class="nxar-slide-counter">{i + 1}/{total}</div>
        </div>
        {estilo_extra}
        <div class="nxar-slide-icon" style="color:{c1};font-size:28px">{icon}</div>
        <h2 class="nxar-slide-titulo" style="font-size:{_afs(tit,'slide')}">{tit}</h2>
        {sub_p_default}
        {_slide_body(tipo, s, vis, c1, c2)}
        {tpl_m}
      </div>
      {logo_html}
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


def _render_reel(empresa, contenido, estructura, estilo=None) -> str:
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
        "problema":   "linear-gradient(145deg,#1e1028,#16213e)",
        "desarrollo": "linear-gradient(145deg,#1e1028,#16213e)",
        "solucion":   "linear-gradient(145deg,#0d1b2e,#0a2040)",
        "ejemplo":    "linear-gradient(145deg,#0d1b2e,#16213e)",
        "beneficio":  "linear-gradient(145deg,#0d2137,#0a1628)",
        "cta":        f"linear-gradient(145deg,{c2},{c1})",
    }
    tipo_label = {
        "hook": "HOOK", "problema": "PROBLEMA", "desarrollo": "DESARROLLO",
        "solucion": "SOLUCIÓN", "ejemplo": "EJEMPLO", "beneficio": "BENEFICIO", "cta": "CTA",
    }
    transicion_sym = {"corte": "✦", "fundido": "◌"}
    estilo_id = (estilo or {}).get("id", "hook_solucion")
    estilo_nombre_reel = (estilo or {}).get("nombre", "")

    # Color de acento del header por estilo (identidad visual fuerte)
    _header_colors = {
        "hook_solucion":      (c1, c2),
        "error_comun":        ("#ef4444", "#dc2626"),
        "tutorial_rapido":    ("#f97316", "#ea580c"),
        "caso_exito":         ("#8b5cf6", "#7c3aed"),
        "tendencia_educativa":("#06b6d4", "#0891b2"),
    }
    h_c1, h_c2 = _header_colors.get(estilo_id, (c1, c2))

    # Etiquetas de escena por estilo
    _labels_estilo = {
        "hook_solucion":     {1: "HOOK", 2: "RETO", 3: "SOLUCIÓN", 4: "RESULTADO", 5: "CTA"},
        "error_comun":       {1: "HOOK", 2: "❌ ERROR", 3: "✓ CORRECCIÓN", 4: "RESULTADO", 5: "CTA"},
        "tutorial_rapido":   {1: "INTRO", 2: "PASO 01", 3: "PASO 02", 4: "PASO 03", 5: "CTA"},
        "caso_exito":        {1: "HOOK", 2: "CLIENTE", 3: "DESAFÍO", 4: "RESULTADO", 5: "CTA"},
        "tendencia_educativa":{1: "CONTEXTO", 2: "TENDENCIA", 3: "DATOS", 4: "IMPACTO", 5: "ACCIÓN"},
    }
    # Backgrounds por estilo y número de escena (sobreescribe tipo_bg)
    _bgs_estilo = {
        "hook_solucion": {
            1: f"linear-gradient(145deg,{c1},{c2})",
            3: "linear-gradient(145deg,#062020,#041818)",
            4: "linear-gradient(145deg,#0a1e30,#061428)",
            5: f"linear-gradient(145deg,{c2},{c1})",
        },
        "error_comun": {
            2: "linear-gradient(145deg,#2d0808,#1a0505)",
            3: "linear-gradient(145deg,#082d08,#051505)",
        },
        "tutorial_rapido": {
            1: "linear-gradient(145deg,#1a0a00,#140800)",
            2: "linear-gradient(145deg,#0a1520,#081220)",
            3: "linear-gradient(145deg,#0a1520,#081220)",
            4: "linear-gradient(145deg,#0a1520,#081220)",
            5: f"linear-gradient(145deg,{c1},{c2})",
        },
        "caso_exito": {
            2: "linear-gradient(145deg,#1a0a2e,#0f0828)",
            3: "linear-gradient(145deg,#1a0a0e,#14080c)",
            4: "linear-gradient(145deg,#0a200e,#08180c)",
        },
        "tendencia_educativa": {
            1: "linear-gradient(145deg,#0a1520,#061220)",
            2: "linear-gradient(145deg,#1a1500,#141100)",
            3: "linear-gradient(145deg,#001a1a,#00121a)",
            4: "linear-gradient(145deg,#1a0a0e,#14080c)",
            5: f"linear-gradient(145deg,{c1},{c2})",
        },
    }

    def _escena_label(num: int, tipo: str) -> str:
        custom = _labels_estilo.get(estilo_id, {}).get(num)
        return custom if custom else tipo_label.get(tipo, tipo.upper())

    def _escena_bg(num: int, tipo: str, default_bg: str) -> str:
        return _bgs_estilo.get(estilo_id, {}).get(num, default_bg)

    escenas_html = ""
    for e in escenas:
        tipo = e.get("tipo", "desarrollo")
        num = e.get("numero", escenas.index(e) + 1)
        bg_default = tipo_bg.get(tipo, "linear-gradient(145deg,#1a1a2e,#16213e)")
        bg = _escena_bg(num, tipo, bg_default)
        label = _escena_label(num, tipo)
        rango = _s(e.get("rango", ""), 10)
        trans = e.get("transicion", "corte")
        trans_sym = transicion_sym.get(trans, "•")

        escenas_html += f"""
    <div class="nxar-escena">
      <div class="nxar-escena-frame" style="background:{bg}">
        {vis["pattern"] if tipo in ("hook", "cta") else ""}
        <span class="nxar-escena-label">{label}</span>
        {_escena_visual(tipo, vis, c1, c2, num)}
        <p class="nxar-escena-texto">{_s(e.get('texto_pantalla', e.get('texto', '')), 60)}</p>
      </div>
      <div class="nxar-escena-meta">
        <span class="nxar-escena-rango">⏱ {rango}</span>
        <span class="nxar-escena-trans" title="{trans}">{trans_sym}</span>
      </div>
    </div>"""

    estilo_tag = f' · <span style="color:{h_c1};font-weight:700">{estilo_nombre_reel}</span>' if estilo_nombre_reel else ""

    return f"""
<div class="nxar-stage nxar-reel-stage">
  <div class="nxar-reel-header" style="background:linear-gradient(135deg,{h_c1}28,{h_c2}18);border-color:{h_c1}44">
    <div class="nxar-reel-meta">
      <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{h_c1},{h_c2})">{initial}</div>
      <span class="nxar-reel-nombre">{_s(nombre, 20)}</span>
      <span class="nxar-reel-cat" style="color:{h_c1}">{vis['icon']} {vis['label']}</span>
      <span class="nxar-reel-dur">🎬 {duracion}</span>
    </div>
    <div class="nxar-reel-hook-txt">"{hook_txt}"</div>
  </div>
  <div class="nxar-reel-timeline-label">STORYBOARD · {len(escenas)} escenas{estilo_tag}</div>
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
