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
# Para reemplazar por imagen real: cambiar solo la función correspondiente
# y devolver <img src="url_de_api"> en su lugar.
# ══════════════════════════════════════════════════════════════════════════════

def _s(text, maxlen=80):
    """Trunca y escapa texto para HTML."""
    return str(text or "")[:maxlen].replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _render_post(empresa, contenido, estructura) -> str:
    c1 = empresa.color_principal
    c2 = empresa.color_secundario
    nombre = empresa.nombre_empresa
    initial = nombre[0].upper()
    ig_user = "@" + nombre.lower().replace(" ", "_")
    titulo = _s(contenido.titulo, 70)
    copy1 = _s(contenido.copy.split("\n")[0], 110)
    cta = _s(contenido.cta or "Contáctanos →", 50)

    return f"""
<div class="nxar-stage nxar-post-stage">
  <div class="nxar-chrome-wrap">
    <!-- Header de cuenta Instagram -->
    <div class="nxar-ig-header">
      <div class="nxar-ig-avatar" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
      <div class="nxar-ig-account">
        <span class="nxar-ig-username">{ig_user}</span>
        <span class="nxar-ig-badge">Publicidad</span>
      </div>
      <span class="nxar-ig-dots">⋯</span>
    </div>
    <!-- Imagen 1:1 -->
    <div class="nxar-post-frame" style="background:linear-gradient(145deg,{c1} 0%,{c2} 100%)">
      <!-- Elementos geométricos de fondo -->
      <div class="nxar-geo nxar-geo--circle1" style="background:rgba(255,255,255,0.07)"></div>
      <div class="nxar-geo nxar-geo--circle2" style="background:rgba(255,255,255,0.04)"></div>
      <div class="nxar-geo nxar-geo--line" style="background:rgba(255,255,255,0.06)"></div>
      <!-- Contenido -->
      <div class="nxar-post-content">
        <div class="nxar-post-top">
          <div class="nxar-logo-chip">{_s(nombre, 14)}</div>
        </div>
        <div class="nxar-post-body">
          <h2 class="nxar-post-titulo">{titulo}</h2>
          <p class="nxar-post-copy">{copy1}</p>
        </div>
        <div class="nxar-post-bottom">
          <div class="nxar-post-cta">{cta}</div>
        </div>
      </div>
    </div>
    <!-- Footer Instagram -->
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

    sticker_html = {
        "encuesta": lambda: f'<div class="nxar-sticker nxar-sticker--encuesta"><span>Encuesta</span><div class="nxar-encuesta-op" style="border-color:{c1}">Sí 👍</div><div class="nxar-encuesta-op">No 👎</div></div>',
        "deslizador": lambda: f'<div class="nxar-sticker nxar-sticker--deslizador">😍 Desliza para reaccionar<div class="nxar-deslizador-track"><div class="nxar-deslizador-thumb" style="background:{c1}">😍</div></div></div>',
        "link": lambda: f'<div class="nxar-sticker nxar-sticker--link" style="border-color:{c1};color:{c1}">🔗 Ver más</div>',
    }

    screens_html = ""
    total = len(pantallas) or 3
    for i, p in enumerate(pantallas[:3]):
        bg = p.get("color_fondo", c1 if i == 0 else c2 if i == 1 else "#0f172a")
        sk = p.get("sticker", "link")
        sk_fn = sticker_html.get(sk, sticker_html["link"])
        dur = p.get("duracion", "7s")
        screens_html += f"""
    <div class="nxar-story-screen" style="background:{'linear-gradient(145deg,' + c1 + ',' + c2 + ')' if i == 0 else bg}">
      <!-- Barras de progreso -->
      <div class="nxar-story-bars">
        {"".join(f'<div class="nxar-story-bar {"nxar-story-bar--done" if j < i else "nxar-story-bar--active" if j == i else ""}"></div>' for j in range(total))}
      </div>
      <!-- Cuenta -->
      <div class="nxar-story-account">
        <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
        <span class="nxar-story-username">{_s(nombre, 20)}</span>
        <span class="nxar-story-time">{dur}</span>
        <span class="nxar-story-x">✕</span>
      </div>
      <!-- Contenido central -->
      <div class="nxar-story-body">
        <p class="nxar-story-titulo">{_s(p.get('titulo', ''), 80)}</p>
        {f'<p class="nxar-story-sub">{_s(p.get("subtitulo", ""), 60)}</p>' if p.get("subtitulo") else ""}
        {sk_fn()}
      </div>
      <!-- Zona inferior -->
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

    tipo_bg = {
        "portada":   f"linear-gradient(145deg,{c1},{c2})",
        "problema":  "linear-gradient(145deg,#1a1a2e,#16213e)",
        "contenido": "linear-gradient(145deg,#0f3460,#16213e)",
        "beneficio": "linear-gradient(145deg,#1a1a2e,#0d2137)",
        "cierre":    "linear-gradient(145deg,#162032,#1a1a2e)",
        "cta":       f"linear-gradient(145deg,{c2},{c1})",
    }
    tipo_icon = {
        "portada": "✦", "problema": "?", "contenido": "◈",
        "beneficio": "✓", "cierre": "→", "cta": "★",
    }

    slides_html = ""
    for i, s in enumerate(slides):
        tipo = s.get("tipo", "contenido")
        bg = tipo_bg.get(tipo, "linear-gradient(145deg,#1a1a2e,#0f172a)")
        icon = tipo_icon.get(tipo, "•")
        active = "nxar-slide--active" if i == 0 else ""
        slides_html += f"""
    <div class="nxar-slide {active}" data-slide="{i}" style="background:{bg}">
      <!-- Elementos geométricos -->
      <div class="nxar-geo nxar-geo--circle1" style="background:rgba(255,255,255,0.05)"></div>
      <div class="nxar-geo nxar-geo--circle2" style="background:rgba(255,255,255,0.03)"></div>
      <div class="nxar-slide-content">
        <div class="nxar-slide-header">
          <div class="nxar-slide-tipo-badge">{tipo.upper()}</div>
          <div class="nxar-slide-counter">{i+1}/{total}</div>
        </div>
        <div class="nxar-slide-icon" style="color:{c1}">{icon}</div>
        <h2 class="nxar-slide-titulo">{_s(s.get('titulo', ''), 80)}</h2>
        {f'<p class="nxar-slide-sub">{_s(s.get("subtitulo", ""), 70)}</p>' if s.get("subtitulo") else ''}
      </div>
      {f'<div class="nxar-slide-logo" style="color:rgba(255,255,255,0.3)">{_s(nombre,12)}</div>' if i == 0 or i == total-1 else ''}
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

    tipo_bg = {
        "hook":       f"linear-gradient(145deg,{c1},{c2})",
        "desarrollo": "linear-gradient(145deg,#1a1a2e,#16213e)",
        "ejemplo":    "linear-gradient(145deg,#0f3460,#16213e)",
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

        escenas_html += f"""
    <div class="nxar-escena">
      <div class="nxar-escena-frame" style="background:{bg}">
        <span class="nxar-escena-label">{label}</span>
        <p class="nxar-escena-texto">{_s(e.get('texto', ''), 60)}</p>
      </div>
      <div class="nxar-escena-meta">
        <span class="nxar-escena-rango">⏱ {rango}</span>
        <span class="nxar-escena-trans" title="{trans}">{trans_sym}</span>
      </div>
    </div>"""

    return f"""
<div class="nxar-stage nxar-reel-stage">
  <!-- Header Reel -->
  <div class="nxar-reel-header" style="background:linear-gradient(135deg,{c1}22,{c2}22);border-color:{c1}33">
    <div class="nxar-reel-meta">
      <div class="nxar-ig-avatar nxar-ig-avatar--sm" style="background:linear-gradient(135deg,{c1},{c2})">{initial}</div>
      <span class="nxar-reel-nombre">{_s(nombre, 20)}</span>
      <span class="nxar-reel-dur">🎬 {duracion}</span>
    </div>
    <div class="nxar-reel-hook-txt">"{hook_txt}"</div>
  </div>
  <!-- Timeline label -->
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
