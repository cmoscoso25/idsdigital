"""
Biblioteca Visual Interna — Nexa AI
SVG/HTML profesionales para posts y carruseles Instagram.
Sin imágenes externas: todo generado con SVG puro + colores de marca.
"""


# ── API pública ────────────────────────────────────────────────────────────────

def get_visual_pack(categoria: str, c1: str, c2: str) -> dict:
    """Retorna el pack visual completo para una categoría y colores de marca."""
    fn = _HEROES.get(categoria, _hero_tecnologia)
    return {
        "hero":        fn(c1, c2),
        "slide_visuals": _slide_visuals(categoria, c1, c2),
        "categoria":   categoria,
    }


def get_slide_visual(tipo_slide: str, categoria: str, c1: str, c2: str) -> str:
    """Retorna el elemento visual específico para un tipo de slide de carrusel."""
    pack = _slide_visuals(categoria, c1, c2)
    return pack.get(tipo_slide, pack.get("contenido", ""))


# ── Heroes por categoría ──────────────────────────────────────────────────────

def _hero_software(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <linearGradient id="vs_sg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{c2}" stop-opacity="0.7"/>
    </linearGradient>
    <filter id="vs_glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Laptop body -->
  <rect x="30" y="14" width="260" height="168" rx="9" fill="#0a0d14" stroke="url(#vs_sg)" stroke-width="1.5"/>
  <rect x="38" y="22" width="244" height="152" rx="5" fill="#060810"/>
  <!-- Window bar -->
  <rect x="38" y="22" width="244" height="22" rx="5" fill="{c1}28"/>
  <circle cx="50" cy="33" r="4" fill="#ef4444" opacity="0.75"/>
  <circle cx="62" cy="33" r="4" fill="#f59e0b" opacity="0.75"/>
  <circle cx="74" cy="33" r="4" fill="#22c55e" opacity="0.75"/>
  <text x="160" y="37" text-anchor="middle" font-size="8" fill="white" opacity="0.3" font-family="monospace">nexa-dashboard.app</text>
  <!-- Sidebar nav -->
  <rect x="38" y="44" width="46" height="130" fill="{c2}14"/>
  <rect x="46" y="54" width="30" height="7" rx="2" fill="{c1}" opacity="0.5"/>
  <rect x="46" y="66" width="30" height="7" rx="2" fill="white" opacity="0.1"/>
  <rect x="46" y="78" width="30" height="7" rx="2" fill="white" opacity="0.1"/>
  <rect x="46" y="90" width="30" height="7" rx="2" fill="white" opacity="0.08"/>
  <rect x="46" y="102" width="30" height="7" rx="2" fill="white" opacity="0.08"/>
  <!-- KPI cards row -->
  <rect x="92" y="50" width="56" height="34" rx="5" fill="#0f1520" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="120" y="64" text-anchor="middle" font-size="11" fill="{c1}" font-weight="700" font-family="sans-serif" filter="url(#vs_glow)">98%</text>
  <text x="120" y="76" text-anchor="middle" font-size="6" fill="white" opacity="0.45" font-family="sans-serif">UPTIME</text>
  <rect x="154" y="50" width="56" height="34" rx="5" fill="#0f1520" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="182" y="64" text-anchor="middle" font-size="11" fill="{c2}" font-weight="700" font-family="sans-serif">4.2x</text>
  <text x="182" y="76" text-anchor="middle" font-size="6" fill="white" opacity="0.45" font-family="sans-serif">ROI</text>
  <rect x="216" y="50" width="56" height="34" rx="5" fill="#0f1520" stroke="{c1}" stroke-width="0.6" stroke-opacity="0.25"/>
  <text x="244" y="64" text-anchor="middle" font-size="11" fill="white" opacity="0.65" font-weight="700" font-family="sans-serif">+48%</text>
  <text x="244" y="76" text-anchor="middle" font-size="6" fill="white" opacity="0.4" font-family="sans-serif">CREC.</text>
  <!-- Chart area -->
  <rect x="92" y="90" width="180" height="76" rx="5" fill="#0a0d14"/>
  <rect x="92" y="90" width="180" height="14" rx="5" fill="{c1}14"/>
  <text x="100" y="101" font-size="7" fill="{c1}" opacity="0.7" font-family="sans-serif" font-weight="600">RENDIMIENTO MENSUAL</text>
  <!-- Bar chart -->
  <g>
    <rect x="99"  y="136" width="14" height="22" rx="2" fill="{c1}" opacity="0.3"/>
    <rect x="117" y="126" width="14" height="32" rx="2" fill="{c1}" opacity="0.45"/>
    <rect x="135" y="118" width="14" height="40" rx="2" fill="{c1}" opacity="0.6"/>
    <rect x="153" y="108" width="14" height="50" rx="2" fill="{c1}" opacity="0.75"/>
    <rect x="171" y="113" width="14" height="45" rx="2" fill="{c2}" opacity="0.8"/>
    <rect x="189" y="105" width="14" height="53" rx="2" fill="{c1}" opacity="0.85"/>
    <rect x="207" y="100" width="14" height="58" rx="2" fill="{c1}"/>
    <rect x="225" y="103" width="14" height="55" rx="2" fill="{c2}" opacity="0.9"/>
    <rect x="243" y="97"  width="14" height="61" rx="2" fill="{c1}" opacity="0.95"/>
  </g>
  <!-- Trend line -->
  <polyline points="106,132 124,121 142,114 160,104 178,109 196,101 214,96 232,99 250,93" fill="none" stroke="{c1}" stroke-width="2" opacity="0.9" filter="url(#vs_glow)"/>
  <circle cx="250" cy="93" r="3.5" fill="{c1}" filter="url(#vs_glow)"/>
  <!-- Laptop stand -->
  <rect x="8" y="182" width="304" height="10" rx="5" fill="#0a0d14" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.3"/>
  <rect x="125" y="192" width="70" height="8" rx="4" fill="{c1}" opacity="0.12"/>
</svg>"""


def _hero_ia(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <filter id="ai_glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="ai_sm"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Background grid subtle -->
  <rect width="320" height="210" fill="#04020a"/>
  <!-- Neural network connections -->
  <!-- L1→L2 -->
  <line x1="52" y1="48"  x2="132" y2="38"  stroke="{c1}" stroke-width="0.6" opacity="0.35"/>
  <line x1="52" y1="48"  x2="132" y2="78"  stroke="{c1}" stroke-width="0.6" opacity="0.3"/>
  <line x1="52" y1="48"  x2="132" y2="118" stroke="{c1}" stroke-width="0.6" opacity="0.2"/>
  <line x1="52" y1="105" x2="132" y2="38"  stroke="{c1}" stroke-width="0.6" opacity="0.3"/>
  <line x1="52" y1="105" x2="132" y2="78"  stroke="{c1}" stroke-width="0.6" opacity="0.4"/>
  <line x1="52" y1="105" x2="132" y2="118" stroke="{c1}" stroke-width="0.6" opacity="0.35"/>
  <line x1="52" y1="105" x2="132" y2="158" stroke="{c1}" stroke-width="0.6" opacity="0.2"/>
  <line x1="52" y1="162" x2="132" y2="78"  stroke="{c1}" stroke-width="0.6" opacity="0.25"/>
  <line x1="52" y1="162" x2="132" y2="118" stroke="{c1}" stroke-width="0.6" opacity="0.35"/>
  <line x1="52" y1="162" x2="132" y2="158" stroke="{c1}" stroke-width="0.6" opacity="0.4"/>
  <!-- L2→L3 -->
  <line x1="132" y1="38"  x2="210" y2="55"  stroke="{c2}" stroke-width="0.7" opacity="0.45"/>
  <line x1="132" y1="38"  x2="210" y2="105" stroke="{c2}" stroke-width="0.7" opacity="0.3"/>
  <line x1="132" y1="78"  x2="210" y2="55"  stroke="{c2}" stroke-width="0.7" opacity="0.55"/>
  <line x1="132" y1="78"  x2="210" y2="105" stroke="{c2}" stroke-width="0.7" opacity="0.5"/>
  <line x1="132" y1="78"  x2="210" y2="155" stroke="{c2}" stroke-width="0.7" opacity="0.3"/>
  <line x1="132" y1="118" x2="210" y2="55"  stroke="{c2}" stroke-width="0.7" opacity="0.35"/>
  <line x1="132" y1="118" x2="210" y2="105" stroke="{c2}" stroke-width="0.7" opacity="0.6"/>
  <line x1="132" y1="118" x2="210" y2="155" stroke="{c2}" stroke-width="0.7" opacity="0.5"/>
  <line x1="132" y1="158" x2="210" y2="105" stroke="{c2}" stroke-width="0.7" opacity="0.4"/>
  <line x1="132" y1="158" x2="210" y2="155" stroke="{c2}" stroke-width="0.7" opacity="0.55"/>
  <!-- L3→L4 -->
  <line x1="210" y1="55"  x2="276" y2="80"  stroke="{c1}" stroke-width="0.8" opacity="0.5"/>
  <line x1="210" y1="55"  x2="276" y2="130" stroke="{c1}" stroke-width="0.8" opacity="0.3"/>
  <line x1="210" y1="105" x2="276" y2="80"  stroke="{c1}" stroke-width="0.8" opacity="0.6"/>
  <line x1="210" y1="105" x2="276" y2="130" stroke="{c1}" stroke-width="0.8" opacity="0.65"/>
  <line x1="210" y1="155" x2="276" y2="80"  stroke="{c1}" stroke-width="0.8" opacity="0.35"/>
  <line x1="210" y1="155" x2="276" y2="130" stroke="{c1}" stroke-width="0.8" opacity="0.5"/>
  <!-- Layer 1 nodes (input) -->
  <circle cx="52" cy="48"  r="8"  fill="{c1}" opacity="0.6" filter="url(#ai_sm)"/>
  <circle cx="52" cy="105" r="9"  fill="{c1}" opacity="0.8" filter="url(#ai_glow)"/>
  <circle cx="52" cy="162" r="7"  fill="{c1}" opacity="0.55" filter="url(#ai_sm)"/>
  <!-- Layer 2 nodes (hidden 1) -->
  <circle cx="132" cy="38"  r="7"  fill="{c2}" opacity="0.65"/>
  <circle cx="132" cy="78"  r="10" fill="{c2}" opacity="0.9" filter="url(#ai_glow)"/>
  <circle cx="132" cy="118" r="9"  fill="{c2}" opacity="0.8" filter="url(#ai_sm)"/>
  <circle cx="132" cy="158" r="6"  fill="{c2}" opacity="0.5"/>
  <!-- Layer 3 nodes (hidden 2) -->
  <circle cx="210" cy="55"  r="8"  fill="{c1}" opacity="0.7"/>
  <circle cx="210" cy="105" r="12" fill="{c1}" opacity="1"   filter="url(#ai_glow)"/>
  <circle cx="210" cy="155" r="7"  fill="{c1}" opacity="0.65"/>
  <!-- Layer 4 nodes (output) -->
  <circle cx="276" cy="80"  r="9"  fill="{c2}" opacity="0.85" filter="url(#ai_sm)"/>
  <circle cx="276" cy="130" r="11" fill="{c2}" opacity="1"    filter="url(#ai_glow)"/>
  <!-- Node labels -->
  <text x="210" y="109" text-anchor="middle" font-size="8" fill="white" font-weight="700" font-family="monospace">AI</text>
  <text x="276" y="134" text-anchor="middle" font-size="7" fill="white" font-weight="700" font-family="monospace">OUT</text>
  <!-- AI Chip decorative -->
  <rect x="8" y="8" width="36" height="36" rx="5" fill="none" stroke="{c1}" stroke-width="1.2" opacity="0.6"/>
  <rect x="14" y="14" width="24" height="24" rx="3" fill="{c1}" opacity="0.12"/>
  <g stroke="{c1}" stroke-width="1" opacity="0.5">
    <line x1="16" y1="8"  x2="16" y2="3"/><line x1="22" y1="8" x2="22" y2="3"/><line x1="28" y1="8" x2="28" y2="3"/>
    <line x1="16" y1="44" x2="16" y2="49"/><line x1="22" y1="44" x2="22" y2="49"/><line x1="28" y1="44" x2="28" y2="49"/>
    <line x1="8"  y1="16" x2="3"  y2="16"/><line x1="8" y1="22" x2="3" y2="22"/><line x1="8" y1="28" x2="3" y2="28"/>
    <line x1="44" y1="16" x2="49" y2="16"/><line x1="44" y1="22" x2="49" y2="22"/><line x1="44" y1="28" x2="49" y2="28"/>
  </g>
  <text x="26" y="29" text-anchor="middle" font-size="9" fill="{c1}" font-weight="800" font-family="monospace" filter="url(#ai_sm)">AI</text>
  <!-- Floating metrics -->
  <rect x="256" y="8" width="56" height="22" rx="4" fill="{c1}22" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="284" y="23" text-anchor="middle" font-size="9" fill="{c1}" font-weight="700" font-family="sans-serif">98.5%</text>
  <rect x="256" y="35" width="56" height="18" rx="4" fill="{c2}18" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="284" y="48" text-anchor="middle" font-size="8" fill="{c2}" font-weight="600" font-family="sans-serif">Precisión</text>
</svg>"""


def _hero_automatizacion(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <filter id="au_glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="320" height="210" fill="#030610"/>
  <!-- Process flow: 5 connected steps horizontal -->
  <!-- Connecting lines -->
  <line x1="74" y1="90" x2="104" y2="90" stroke="{c1}" stroke-width="1.5" opacity="0.5" stroke-dasharray="4,3"/>
  <line x1="174" y1="90" x2="204" y2="90" stroke="{c1}" stroke-width="1.5" opacity="0.5" stroke-dasharray="4,3"/>
  <line x1="244" y1="90" x2="274" y2="90" stroke="{c2}" stroke-width="1.5" opacity="0.6" stroke-dasharray="4,3"/>
  <!-- Arrow heads -->
  <polygon points="104,86 112,90 104,94" fill="{c1}" opacity="0.6"/>
  <polygon points="204,86 212,90 204,94" fill="{c1}" opacity="0.6"/>
  <polygon points="274,86 282,90 274,94" fill="{c2}" opacity="0.7"/>
  <!-- Step boxes -->
  <!-- Step 1: Input -->
  <rect x="14" y="66" width="60" height="48" rx="8" fill="#0a0e1a" stroke="{c1}" stroke-width="1.5" stroke-opacity="0.7"/>
  <rect x="14" y="66" width="60" height="16" rx="8" fill="{c1}33"/>
  <text x="44" y="78" text-anchor="middle" font-size="7" fill="{c1}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">ENTRADA</text>
  <rect x="22" y="88" width="44" height="5" rx="2.5" fill="white" opacity="0.12"/>
  <rect x="22" y="96" width="32" height="5" rx="2.5" fill="white" opacity="0.08"/>
  <!-- Step 2: Process -->
  <rect x="112" y="66" width="62" height="48" rx="8" fill="#0a0e1a" stroke="{c2}" stroke-width="1.5" stroke-opacity="0.7"/>
  <rect x="112" y="66" width="62" height="16" rx="8" fill="{c2}2a"/>
  <text x="143" y="78" text-anchor="middle" font-size="7" fill="{c2}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">PROCESO</text>
  <!-- Gear icon inside -->
  <g transform="translate(143,96)" opacity="0.7">
    <circle r="8" fill="none" stroke="{c2}" stroke-width="1.2"/>
    <circle r="4" fill="{c2}" opacity="0.3"/>
    <g stroke="{c2}" stroke-width="1">
      <line x1="0" y1="-8" x2="0" y2="-11"/><line x1="0" y1="8" x2="0" y2="11"/>
      <line x1="-8" y1="0" x2="-11" y2="0"/><line x1="8" y1="0" x2="11" y2="0"/>
    </g>
  </g>
  <!-- Step 3: Validate -->
  <rect x="212" y="66" width="62" height="48" rx="8" fill="#0a0e1a" stroke="{c1}" stroke-width="1.5" stroke-opacity="0.65"/>
  <rect x="212" y="66" width="62" height="16" rx="8" fill="{c1}22"/>
  <text x="243" y="78" text-anchor="middle" font-size="7" fill="{c1}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">VALIDAR</text>
  <text x="243" y="102" text-anchor="middle" font-size="18" fill="{c1}" opacity="0.7" filter="url(#au_glow)">✓</text>
  <!-- Step 4: Output -->
  <rect x="282" y="66" width="28" height="48" rx="8" fill="{c2}22" stroke="{c2}" stroke-width="1.5" stroke-opacity="0.8"/>
  <text x="296" y="78" text-anchor="middle" font-size="6.5" fill="{c2}" font-weight="700" font-family="sans-serif" writing-mode="vertical-rl">SALIDA</text>
  <circle cx="296" cy="102" r="6" fill="{c2}" opacity="0.8" filter="url(#au_glow)"/>
  <!-- Status indicators below each step -->
  <circle cx="44"  cy="128" r="4" fill="#22c55e" opacity="0.9" filter="url(#au_glow)"/>
  <circle cx="143" cy="128" r="4" fill="{c1}"    opacity="0.8"/>
  <circle cx="243" cy="128" r="4" fill="{c1}"    opacity="0.7"/>
  <circle cx="296" cy="128" r="4" fill="{c2}"    opacity="0.9"/>
  <text x="44"  y="143" text-anchor="middle" font-size="6.5" fill="#22c55e" opacity="0.75" font-family="sans-serif">Activo</text>
  <text x="143" y="143" text-anchor="middle" font-size="6.5" fill="{c1}" opacity="0.65" font-family="sans-serif">En curso</text>
  <text x="243" y="143" text-anchor="middle" font-size="6.5" fill="{c1}" opacity="0.6" font-family="sans-serif">Pendiente</text>
  <text x="296" y="143" text-anchor="middle" font-size="6.5" fill="{c2}" opacity="0.8" font-family="sans-serif">Listo</text>
  <!-- Stats bar -->
  <rect x="14" y="158" width="292" height="38" rx="6" fill="#060910"/>
  <rect x="14" y="158" width="292" height="12" rx="6" fill="{c1}14"/>
  <text x="18" y="169" font-size="7" fill="{c1}" opacity="0.7" font-weight="600" font-family="sans-serif">AUTOMATIZACIÓN ACTIVA</text>
  <text x="300" y="169" text-anchor="end" font-size="7" fill="{c2}" opacity="0.8" font-weight="700" font-family="sans-serif">85% completo</text>
  <rect x="22" y="175" width="278" height="5" rx="2.5" fill="white" opacity="0.06"/>
  <rect x="22" y="175" width="236" height="5" rx="2.5" fill="url(#vs_sg)" opacity="0.8"/>
  <text x="18" y="192" font-size="6.5" fill="white" opacity="0.35" font-family="sans-serif">Tareas procesadas hoy: 1,248</text>
  <text x="300" y="192" text-anchor="end" font-size="6.5" fill="#22c55e" opacity="0.7" font-family="sans-serif">0 errores</text>
</svg>"""


def _hero_marketing(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <filter id="mk_glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="320" height="210" fill="#030810"/>
  <!-- Growth bars (main visual) -->
  <rect x="20" y="148" width="22" height="38" rx="3" fill="{c1}" opacity="0.2"/>
  <rect x="46" y="128" width="22" height="58" rx="3" fill="{c1}" opacity="0.35"/>
  <rect x="72" y="108" width="22" height="78" rx="3" fill="{c1}" opacity="0.5"/>
  <rect x="98" y="85"  width="22" height="101" rx="3" fill="{c1}" opacity="0.65"/>
  <rect x="124" y="68" width="22" height="118" rx="3" fill="{c1}" opacity="0.8"/>
  <rect x="150" y="48" width="22" height="138" rx="3" fill="{c1}" opacity="0.9"/>
  <rect x="176" y="36" width="22" height="150" rx="3" fill="{c2}" opacity="0.95"/>
  <rect x="202" y="28" width="22" height="158" rx="3" fill="{c1}"/>
  <!-- Bar tops glow -->
  <rect x="202" y="28" width="22" height="6" rx="2" fill="{c1}" filter="url(#mk_glow)"/>
  <!-- Trend line -->
  <polyline points="31,144 57,124 83,104 109,81 135,64 161,44 187,32 213,24" fill="none" stroke="{c1}" stroke-width="2.2" opacity="0.9" filter="url(#mk_glow)"/>
  <circle cx="213" cy="24" r="5" fill="{c1}" filter="url(#mk_glow)"/>
  <!-- X axis -->
  <line x1="12" y1="188" x2="240" y2="188" stroke="white" stroke-width="0.8" opacity="0.15"/>
  <!-- Growth badge -->
  <rect x="248" y="18" width="66" height="36" rx="6" fill="{c1}28" stroke="{c1}" stroke-width="1" stroke-opacity="0.6"/>
  <text x="281" y="32" text-anchor="middle" font-size="14" fill="{c1}" font-weight="900" font-family="sans-serif" filter="url(#mk_glow)">+48%</text>
  <text x="281" y="46" text-anchor="middle" font-size="7.5" fill="white" opacity="0.55" font-family="sans-serif">CRECIMIENTO</text>
  <!-- KPI cards right side -->
  <rect x="248" y="62" width="66" height="30" rx="5" fill="#0a0e1a" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="281" y="74" text-anchor="middle" font-size="9" fill="{c2}" font-weight="700" font-family="sans-serif">3.2%</text>
  <text x="281" y="84" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">CTR promedio</text>
  <rect x="248" y="96" width="66" height="30" rx="5" fill="#0a0e1a" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="281" y="108" text-anchor="middle" font-size="9" fill="{c1}" font-weight="700" font-family="sans-serif">6.1x</text>
  <text x="281" y="118" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">ROAS</text>
  <rect x="248" y="130" width="66" height="30" rx="5" fill="#0a0e1a" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="281" y="142" text-anchor="middle" font-size="9" fill="{c2}" font-weight="700" font-family="sans-serif">12.4k</text>
  <text x="281" y="152" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Leads / mes</text>
  <!-- Month labels -->
  <text x="31"  y="200" text-anchor="middle" font-size="6" fill="white" opacity="0.25" font-family="sans-serif">ENE</text>
  <text x="57"  y="200" text-anchor="middle" font-size="6" fill="white" opacity="0.25" font-family="sans-serif">FEB</text>
  <text x="83"  y="200" text-anchor="middle" font-size="6" fill="white" opacity="0.25" font-family="sans-serif">MAR</text>
  <text x="109" y="200" text-anchor="middle" font-size="6" fill="white" opacity="0.25" font-family="sans-serif">ABR</text>
  <text x="135" y="200" text-anchor="middle" font-size="6" fill="white" opacity="0.25" font-family="sans-serif">MAY</text>
  <text x="161" y="200" text-anchor="middle" font-size="6" fill="{c1}" opacity="0.6" font-family="sans-serif" font-weight="600">JUN</text>
  <text x="187" y="200" text-anchor="middle" font-size="6" fill="{c2}" opacity="0.6" font-family="sans-serif" font-weight="600">JUL</text>
  <text x="213" y="200" text-anchor="middle" font-size="6" fill="{c1}" opacity="0.8" font-family="sans-serif" font-weight="700">AGO</text>
</svg>"""


def _hero_productividad(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <filter id="pr_glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="320" height="210" fill="#030710"/>
  <!-- Kanban-style task board -->
  <!-- Column: Por hacer -->
  <rect x="12" y="8" width="90" height="192" rx="7" fill="#080c18"/>
  <rect x="12" y="8" width="90" height="22" rx="7" fill="{c1}22"/>
  <text x="57" y="23" text-anchor="middle" font-size="8" fill="{c1}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">POR HACER</text>
  <!-- Tasks column 1 -->
  <rect x="18" y="36" width="78" height="32" rx="5" fill="#0d1220" stroke="white" stroke-width="0.5" stroke-opacity="0.1"/>
  <rect x="18" y="36" width="5"  height="32" rx="3" fill="{c1}" opacity="0.6"/>
  <text x="29" y="50" font-size="7.5" fill="white" opacity="0.75" font-family="sans-serif" font-weight="600">Configurar CRM</text>
  <text x="29" y="60" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Prioridad alta</text>
  <rect x="18" y="74" width="78" height="28" rx="5" fill="#0d1220" stroke="white" stroke-width="0.5" stroke-opacity="0.1"/>
  <rect x="18" y="74" width="5"  height="28" rx="3" fill="{c2}" opacity="0.55"/>
  <text x="29" y="86" font-size="7.5" fill="white" opacity="0.7" font-family="sans-serif">Análisis datos</text>
  <text x="29" y="96" font-size="6.5" fill="white" opacity="0.35" font-family="sans-serif">Media</text>
  <rect x="18" y="108" width="78" height="28" rx="5" fill="#0d1220" stroke="white" stroke-width="0.5" stroke-opacity="0.08"/>
  <rect x="18" y="108" width="5"  height="28" rx="3" fill="white" opacity="0.2"/>
  <text x="29" y="120" font-size="7.5" fill="white" opacity="0.5" font-family="sans-serif">Review semanal</text>
  <!-- Column: En curso -->
  <rect x="114" y="8" width="90" height="192" rx="7" fill="#080c18"/>
  <rect x="114" y="8" width="90" height="22" rx="7" fill="{c2}20"/>
  <text x="159" y="23" text-anchor="middle" font-size="8" fill="{c2}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">EN CURSO</text>
  <rect x="120" y="36" width="78" height="32" rx="5" fill="{c2}18" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.4"/>
  <rect x="120" y="36" width="5"  height="32" rx="3" fill="{c2}" opacity="0.9"/>
  <text x="131" y="50" font-size="7.5" fill="white" opacity="0.85" font-family="sans-serif" font-weight="700">Lanzar campaña</text>
  <text x="131" y="60" font-size="6.5" fill="{c2}" opacity="0.7" font-family="sans-serif">70% completado</text>
  <!-- Progress bar -->
  <rect x="131" y="63" width="60" height="3" rx="1.5" fill="white" opacity="0.1"/>
  <rect x="131" y="63" width="42" height="3" rx="1.5" fill="{c2}" opacity="0.8"/>
  <rect x="120" y="74" width="78" height="28" rx="5" fill="{c1}14" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.3"/>
  <rect x="120" y="74" width="5"  height="28" rx="3" fill="{c1}" opacity="0.8"/>
  <text x="131" y="86" font-size="7.5" fill="white" opacity="0.8" font-family="sans-serif">Integrar API</text>
  <text x="131" y="96" font-size="6.5" fill="{c1}" opacity="0.6" font-family="sans-serif">45% completado</text>
  <!-- Column: Listo -->
  <rect x="216" y="8" width="90" height="192" rx="7" fill="#080c18"/>
  <rect x="216" y="8" width="90" height="22" rx="7" fill="#22c55e22"/>
  <text x="261" y="23" text-anchor="middle" font-size="8" fill="#22c55e" font-weight="700" font-family="sans-serif" letter-spacing="0.5">LISTO</text>
  <rect x="222" y="36" width="78" height="28" rx="5" fill="#22c55e0f" stroke="#22c55e" stroke-width="0.8" stroke-opacity="0.35"/>
  <rect x="222" y="36" width="5"  height="28" rx="3" fill="#22c55e" opacity="0.8"/>
  <text x="233" y="48" font-size="7.5" fill="white" opacity="0.7" font-family="sans-serif">Setup inicial</text>
  <text x="233" y="58" font-size="7" fill="#22c55e" opacity="0.65" font-family="sans-serif">✓ Completado</text>
  <rect x="222" y="70" width="78" height="28" rx="5" fill="#22c55e0f" stroke="#22c55e" stroke-width="0.8" stroke-opacity="0.3"/>
  <rect x="222" y="70" width="5"  height="28" rx="3" fill="#22c55e" opacity="0.7"/>
  <text x="233" y="82" font-size="7.5" fill="white" opacity="0.65" font-family="sans-serif">Onboarding</text>
  <text x="233" y="92" font-size="7" fill="#22c55e" opacity="0.6" font-family="sans-serif">✓ Completado</text>
  <rect x="222" y="104" width="78" height="28" rx="5" fill="#22c55e0f" stroke="#22c55e" stroke-width="0.8" stroke-opacity="0.25"/>
  <rect x="222" y="104" width="5"  height="28" rx="3" fill="#22c55e" opacity="0.6"/>
  <text x="233" y="116" font-size="7.5" fill="white" opacity="0.55" font-family="sans-serif">Documentación</text>
  <text x="233" y="126" font-size="7" fill="#22c55e" opacity="0.5" font-family="sans-serif">✓ Completado</text>
  <!-- Progress ring bottom right -->
  <circle cx="261" cy="168" r="24" fill="none" stroke="white" stroke-width="1" opacity="0.06"/>
  <circle cx="261" cy="168" r="24" fill="none" stroke="{c1}" stroke-width="3" stroke-dasharray="110 151" stroke-dashoffset="-10" stroke-linecap="round" opacity="0.8" filter="url(#pr_glow)"/>
  <text x="261" y="172" text-anchor="middle" font-size="10" fill="{c1}" font-weight="800" font-family="sans-serif">73%</text>
</svg>"""


def _hero_educacion(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <rect width="320" height="210" fill="#03080e"/>
  <!-- Learning cards -->
  <rect x="12" y="18" width="140" height="80" rx="8" fill="#0a1020" stroke="{c1}" stroke-width="1" stroke-opacity="0.5"/>
  <rect x="12" y="18" width="140" height="22" rx="8" fill="{c1}28"/>
  <text x="82" y="33" text-anchor="middle" font-size="8.5" fill="{c1}" font-weight="700" font-family="sans-serif">MÓDULO 1 · FUNDAMENTOS</text>
  <rect x="20" y="46" width="124" height="6" rx="3" fill="white" opacity="0.08"/>
  <rect x="20" y="46" width="90"  height="6" rx="3" fill="{c1}" opacity="0.7"/>
  <text x="18" y="62" font-size="7.5" fill="white" opacity="0.6" font-family="sans-serif">Progreso: 73%</text>
  <text x="148" y="62" text-anchor="end" font-size="7.5" fill="{c1}" font-weight="700" font-family="sans-serif">15/20</text>
  <rect x="20" y="66" width="58" height="18" rx="4" fill="{c1}22" stroke="{c1}" stroke-width="0.7" stroke-opacity="0.5"/>
  <text x="49" y="78" text-anchor="middle" font-size="7.5" fill="{c1}" font-weight="600" font-family="sans-serif">Continuar</text>
  <rect x="84" y="66" width="58" height="18" rx="4" fill="white" opacity="0.05"/>
  <text x="113" y="78" text-anchor="middle" font-size="7.5" fill="white" opacity="0.4" font-family="sans-serif">Evaluación</text>
  <!-- Card 2 -->
  <rect x="168" y="18" width="140" height="80" rx="8" fill="#0a1020" stroke="{c2}" stroke-width="1" stroke-opacity="0.45"/>
  <rect x="168" y="18" width="140" height="22" rx="8" fill="{c2}22"/>
  <text x="238" y="33" text-anchor="middle" font-size="8.5" fill="{c2}" font-weight="700" font-family="sans-serif">MÓDULO 2 · AVANZADO</text>
  <rect x="176" y="46" width="124" height="6" rx="3" fill="white" opacity="0.08"/>
  <rect x="176" y="46" width="40"  height="6" rx="3" fill="{c2}" opacity="0.6"/>
  <text x="174" y="62" font-size="7.5" fill="white" opacity="0.45" font-family="sans-serif">Progreso: 32%</text>
  <text x="300" y="62" text-anchor="end" font-size="7.5" fill="{c2}" font-weight="700" font-family="sans-serif">6/18</text>
  <rect x="176" y="66" width="124" height="18" rx="4" fill="{c2}18" stroke="{c2}" stroke-width="0.7" stroke-opacity="0.4"/>
  <text x="238" y="78" text-anchor="middle" font-size="7.5" fill="{c2}" font-weight="600" font-family="sans-serif">Desbloquear próxima lección</text>
  <!-- Stats row -->
  <rect x="12" y="108" width="92" height="48" rx="7" fill="#0a0f1c" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="58" y="122" text-anchor="middle" font-size="18" fill="{c1}" font-weight="900" font-family="sans-serif">94%</text>
  <text x="58" y="134" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Tasa de completado</text>
  <rect x="114" y="108" width="92" height="48" rx="7" fill="#0a0f1c" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="160" y="122" text-anchor="middle" font-size="18" fill="{c2}" font-weight="900" font-family="sans-serif">4.9</text>
  <text x="160" y="134" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Calificación promedio</text>
  <text x="160" y="142" text-anchor="middle" font-size="10" fill="{c2}" opacity="0.7" font-family="sans-serif">★★★★★</text>
  <rect x="216" y="108" width="92" height="48" rx="7" fill="#0a0f1c" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="262" y="122" text-anchor="middle" font-size="18" fill="{c1}" font-weight="900" font-family="sans-serif">-60%</text>
  <text x="262" y="134" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Tiempo de aprendizaje</text>
  <!-- Progress bars bottom -->
  <text x="14" y="173" font-size="7.5" fill="white" opacity="0.5" font-family="sans-serif">Lecciones completadas esta semana</text>
  <rect x="12"  y="178" width="296" height="7" rx="3.5" fill="white" opacity="0.06"/>
  <rect x="12"  y="178" width="216" height="7" rx="3.5" fill="{c1}" opacity="0.75"/>
  <text x="14" y="195" font-size="6.5" fill="{c1}" opacity="0.65" font-family="sans-serif">15 de 20 lecciones</text>
  <text x="308" y="195" text-anchor="end" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">73%</text>
</svg>"""


def _hero_finanzas(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs><filter id="fi_glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="320" height="210" fill="#030a08"/>
  <!-- Area chart -->
  <polyline points="16,155 46,140 76,125 106,108 136,95 166,78 196,62 226,50 256,38 280,30" fill="none" stroke="{c1}" stroke-width="2" opacity="0.9" filter="url(fi_glow)"/>
  <path d="M16,155 46,140 76,125 106,108 136,95 166,78 196,62 226,50 256,38 280,30 L280,178 L16,178 Z" fill="{c1}" opacity="0.08"/>
  <!-- Axis -->
  <line x1="12" y1="178" x2="308" y2="178" stroke="white" stroke-width="0.8" opacity="0.1"/>
  <!-- KPI cards -->
  <rect x="12"  y="12" width="90" height="44" rx="6" fill="#050f08" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="57"  y="27" text-anchor="middle" font-size="16" fill="{c1}" font-weight="900" font-family="sans-serif" filter="url(fi_glow)">+28%</text>
  <text x="57"  y="40" text-anchor="middle" font-size="7" fill="white" opacity="0.4" font-family="sans-serif">ROI anual</text>
  <rect x="116" y="12" width="90" height="44" rx="6" fill="#050f08" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.45"/>
  <text x="161" y="27" text-anchor="middle" font-size="16" fill="{c2}" font-weight="900" font-family="sans-serif">-42%</text>
  <text x="161" y="40" text-anchor="middle" font-size="7" fill="white" opacity="0.4" font-family="sans-serif">Costos operativos</text>
  <rect x="220" y="12" width="90" height="44" rx="6" fill="#050f08" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="265" y="27" text-anchor="middle" font-size="16" fill="{c1}" font-weight="900" font-family="sans-serif">+18%</text>
  <text x="265" y="40" text-anchor="middle" font-size="7" fill="white" opacity="0.4" font-family="sans-serif">Ingresos</text>
  <!-- Trend data points -->
  <circle cx="46"  cy="140" r="3" fill="{c1}" opacity="0.7"/>
  <circle cx="106" cy="108" r="3" fill="{c1}" opacity="0.75"/>
  <circle cx="166" cy="78"  r="3.5" fill="{c1}" opacity="0.85"/>
  <circle cx="226" cy="50"  r="3.5" fill="{c2}" opacity="0.9"/>
  <circle cx="280" cy="30"  r="4.5" fill="{c1}" opacity="1" filter="url(fi_glow)"/>
  <!-- Tooltip at peak -->
  <rect x="252" y="14" width="52" height="20" rx="4" fill="{c1}22" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="278" y="28" text-anchor="middle" font-size="9" fill="{c1}" font-weight="700" font-family="sans-serif">$2.4M</text>
</svg>"""


def _hero_salud(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs><filter id="sa_glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="320" height="210" fill="#030810"/>
  <!-- Heart rate line -->
  <polyline points="14,100 44,100 58,100 70,60 80,140 90,100 104,100 116,100 128,100 140,60 152,140 162,100 190,100 216,100 230,100 240,55 252,148 262,100 290,100 308,100" fill="none" stroke="{c1}" stroke-width="2.5" opacity="0.85" filter="url(sa_glow)"/>
  <!-- Health KPI cards -->
  <rect x="12"  y="118" width="88" height="44" rx="7" fill="#08101a" stroke="{c1}" stroke-width="0.9" stroke-opacity="0.5"/>
  <text x="56"  y="135" text-anchor="middle" font-size="15" fill="{c1}" font-weight="900" font-family="sans-serif">96%</text>
  <text x="56"  y="148" text-anchor="middle" font-size="7" fill="white" opacity="0.45" font-family="sans-serif">Satisfacción pacientes</text>
  <rect x="116" y="118" width="88" height="44" rx="7" fill="#08101a" stroke="{c2}" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="160" y="135" text-anchor="middle" font-size="15" fill="{c2}" font-weight="900" font-family="sans-serif">-35%</text>
  <text x="160" y="148" text-anchor="middle" font-size="7" fill="white" opacity="0.45" font-family="sans-serif">Tiempo de espera</text>
  <rect x="220" y="118" width="88" height="44" rx="7" fill="#08101a" stroke="{c1}" stroke-width="0.9" stroke-opacity="0.4"/>
  <text x="264" y="135" text-anchor="middle" font-size="15" fill="{c1}" font-weight="900" font-family="sans-serif">98%</text>
  <text x="264" y="148" text-anchor="middle" font-size="7" fill="white" opacity="0.45" font-family="sans-serif">Precisión diagnóstico</text>
  <!-- Medical cross -->
  <rect x="140" y="12" width="40" height="12" rx="4" fill="{c1}" opacity="0.8" filter="url(sa_glow)"/>
  <rect x="146" y="6" width="28" height="24" rx="4" fill="{c1}" opacity="0.8"/>
  <rect x="148" y="8" width="24" height="20" rx="3" fill="white" opacity="0.1"/>
  <!-- Health badge -->
  <rect x="12" y="12" width="120" height="68" rx="8" fill="#08101a" stroke="{c1}" stroke-width="0.9" stroke-opacity="0.4"/>
  <text x="72" y="32" text-anchor="middle" font-size="9" fill="{c1}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">SALUD DIGITAL</text>
  <text x="72" y="48" text-anchor="middle" font-size="8" fill="white" opacity="0.6" font-family="sans-serif">Pacientes atendidos</text>
  <text x="72" y="64" text-anchor="middle" font-size="18" fill="{c1}" font-weight="900" font-family="sans-serif">1,248</text>
  <rect x="198" y="12" width="110" height="68" rx="8" fill="#08101a" stroke="{c2}" stroke-width="0.9" stroke-opacity="0.35"/>
  <text x="253" y="32" text-anchor="middle" font-size="9" fill="{c2}" font-weight="700" font-family="sans-serif" letter-spacing="0.5">BIENESTAR</text>
  <text x="253" y="48" text-anchor="middle" font-size="8" fill="white" opacity="0.5" font-family="sans-serif">Índice de mejora</text>
  <text x="253" y="64" text-anchor="middle" font-size="18" fill="{c2}" font-weight="900" font-family="sans-serif">+42%</text>
</svg>"""


def _hero_tecnologia(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs><filter id="tc_glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="320" height="210" fill="#03060e"/>
  <!-- Circuit board pattern -->
  <g stroke="{c1}" stroke-width="0.9" fill="none" opacity="0.45">
    <line x1="28"  y1="52"  x2="80"  y2="52"/><line x1="80"  y1="52"  x2="80"  y2="96"/>
    <line x1="80"  y1="96"  x2="130" y2="96"/><line x1="130" y1="96"  x2="130" y2="52"/>
    <line x1="130" y1="52"  x2="180" y2="52"/><line x1="180" y1="52"  x2="180" y2="130"/>
    <line x1="50"  y1="96"  x2="50"  y2="148"/><line x1="50"  y1="148" x2="110" y2="148"/>
    <line x1="180" y1="130" x2="240" y2="130"/><line x1="240" y1="130" x2="240" y2="68"/>
    <line x1="240" y1="68"  x2="290" y2="68"/><line x1="290" y1="68"  x2="290" y2="130"/>
    <line x1="110" y1="148" x2="110" y2="168"/><line x1="110" y1="168" x2="200" y2="168"/>
    <line x1="200" y1="168" x2="200" y2="130"/>
  </g>
  <!-- Nodes -->
  <g fill="{c1}">
    <rect x="76"  y="48"  width="8" height="8" rx="1.5" opacity="0.8"/>
    <rect x="176" y="48"  width="8" height="8" rx="1.5" opacity="0.8"/>
    <rect x="126" y="92"  width="8" height="8" rx="1.5" opacity="0.9"/>
    <rect x="46"  y="92"  width="8" height="8" rx="1.5" opacity="0.7"/>
    <rect x="46"  y="144" width="8" height="8" rx="1.5" opacity="0.75"/>
    <rect x="106" y="144" width="8" height="8" rx="1.5" opacity="0.8"/>
    <rect x="176" y="126" width="8" height="8" rx="1.5" opacity="0.85"/>
    <rect x="196" y="164" width="8" height="8" rx="1.5" opacity="0.7"/>
    <rect x="236" y="126" width="8" height="8" rx="1.5" opacity="0.8"/>
    <rect x="286" y="126" width="8" height="8" rx="1.5" opacity="0.75"/>
  </g>
  <!-- Glowing main node -->
  <circle cx="130" cy="96" r="6" fill="{c1}" opacity="0.9" filter="url(tc_glow)"/>
  <circle cx="240" cy="130" r="5" fill="{c2}" opacity="0.9" filter="url(tc_glow)"/>
  <!-- Tech cards -->
  <rect x="12" y="12" width="80" height="32" rx="5" fill="#08101e" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.4"/>
  <text x="52" y="23" text-anchor="middle" font-size="7.5" fill="{c1}" font-weight="700" font-family="sans-serif">99.9% UPTIME</text>
  <text x="52" y="36" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Infraestructura</text>
  <rect x="236" y="12" width="80" height="32" rx="5" fill="#08101e" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="276" y="23" text-anchor="middle" font-size="7.5" fill="{c2}" font-weight="700" font-family="sans-serif">10x VELOCIDAD</text>
  <text x="276" y="36" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Procesamiento</text>
  <rect x="12"  y="168" width="140" height="32" rx="5" fill="#08101e" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="82" y="181" text-anchor="middle" font-size="7.5" fill="{c1}" font-weight="700" font-family="sans-serif">ARQUITECTURA ESCALABLE</text>
  <text x="82" y="193" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Cloud-native · Microservicios</text>
  <rect x="168" y="168" width="140" height="32" rx="5" fill="#08101e" stroke="{c2}" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="238" y="181" text-anchor="middle" font-size="7.5" fill="{c2}" font-weight="700" font-family="sans-serif">SEGURIDAD ENTERPRISE</text>
  <text x="238" y="193" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">ISO 27001 · SOC2</text>
</svg>"""


def _hero_transformacion(c1: str, c2: str) -> str:
    return f"""<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs><filter id="tr_glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="320" height="210" fill="#03050f"/>
  <!-- Hexagonal network -->
  <g fill="none" stroke="{c1}" stroke-width="1.2">
    <polygon points="100,44 120,56 120,80 100,92 80,80 80,56" opacity="0.7"/>
    <polygon points="140,18 160,30 160,54 140,66 120,54 120,30" opacity="0.5"/>
    <polygon points="60,18 80,30 80,54 60,66 40,54 40,30" opacity="0.45"/>
    <polygon points="100,92 120,104 120,128 100,140 80,128 80,104" opacity="0.8"/>
    <polygon points="140,66 160,78 160,102 140,114 120,102 120,78" opacity="0.6"/>
    <polygon points="60,66 80,78 80,102 60,114 40,102 40,78" opacity="0.5"/>
    <polygon points="100,140 120,152 120,176 100,188 80,176 80,152" opacity="0.45"/>
  </g>
  <!-- Hex fills -->
  <polygon points="100,44 120,56 120,80 100,92 80,80 80,56" fill="{c1}" opacity="0.12"/>
  <polygon points="100,92 120,104 120,128 100,140 80,128 80,104" fill="{c1}" opacity="0.18"/>
  <!-- Connecting lines between hexagons -->
  <line x1="120" y1="56" x2="120" y2="54" stroke="{c1}" stroke-width="1" opacity="0.4"/>
  <line x1="80"  y1="56" x2="80"  y2="54" stroke="{c1}" stroke-width="1" opacity="0.4"/>
  <line x1="100" y1="92" x2="100" y2="92" stroke="{c1}" stroke-width="1.5" opacity="0.6"/>
  <!-- Glowing nodes -->
  <circle cx="100" cy="68" r="7" fill="{c1}" opacity="1" filter="url(tr_glow)"/>
  <circle cx="140" cy="42" r="5" fill="{c2}" opacity="0.9" filter="url(tr_glow)"/>
  <circle cx="60"  cy="42" r="5" fill="{c2}" opacity="0.8"/>
  <circle cx="100" cy="116" r="6" fill="{c1}" opacity="0.9" filter="url(tr_glow)"/>
  <circle cx="140" cy="90" r="4" fill="{c2}" opacity="0.75"/>
  <circle cx="60"  cy="90" r="4" fill="{c2}" opacity="0.7"/>
  <!-- Right side: transformation journey -->
  <rect x="186" y="12"  width="124" height="44" rx="7" fill="#08101e" stroke="{c1}" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="248" y="26"  text-anchor="middle" font-size="8" fill="{c1}" font-weight="700" font-family="sans-serif">ANTES DE LA TRANSFORMACIÓN</text>
  <text x="248" y="40"  text-anchor="middle" font-size="13" fill="white" opacity="0.5" font-weight="700" font-family="sans-serif">Procesos manuales</text>
  <!-- Arrow -->
  <line x1="248" y1="58" x2="248" y2="70" stroke="{c1}" stroke-width="2" opacity="0.7"/>
  <polygon points="241,68 255,68 248,78" fill="{c1}" opacity="0.8"/>
  <rect x="186" y="80"  width="124" height="44" rx="7" fill="{c1}22" stroke="{c1}" stroke-width="1" stroke-opacity="0.7"/>
  <text x="248" y="94"  text-anchor="middle" font-size="8" fill="{c1}" font-weight="700" font-family="sans-serif">DESPUÉS · DIGITAL</text>
  <text x="248" y="108" text-anchor="middle" font-size="13" fill="{c1}" font-weight="800" font-family="sans-serif" filter="url(tr_glow)">+92% eficiencia</text>
  <!-- Stats -->
  <rect x="186" y="136" width="58" height="34" rx="5" fill="#08101e" stroke="{c2}" stroke-width="0.7" stroke-opacity="0.4"/>
  <text x="215" y="150" text-anchor="middle" font-size="13" fill="{c2}" font-weight="900" font-family="sans-serif">3.8x</text>
  <text x="215" y="163" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">ROI</text>
  <rect x="252" y="136" width="58" height="34" rx="5" fill="#08101e" stroke="{c1}" stroke-width="0.7" stroke-opacity="0.35"/>
  <text x="281" y="150" text-anchor="middle" font-size="13" fill="{c1}" font-weight="900" font-family="sans-serif">-45%</text>
  <text x="281" y="163" text-anchor="middle" font-size="6.5" fill="white" opacity="0.4" font-family="sans-serif">Costos</text>
</svg>"""


_HEROES = {
    "software":      _hero_software,
    "ia":            _hero_ia,
    "automatizacion":_hero_automatizacion,
    "marketing":     _hero_marketing,
    "productividad": _hero_productividad,
    "educacion":     _hero_educacion,
    "finanzas":      _hero_finanzas,
    "salud":         _hero_salud,
    "tecnologia":    _hero_tecnologia,
    "transformacion":_hero_transformacion,
}


# ── Slide visuals para carrusel ───────────────────────────────────────────────

def _slide_visuals(categoria: str, c1: str, c2: str) -> dict:
    """Retorna dict con HTML visual para cada tipo de slide."""
    return {
        "portada":     _sv_portada(categoria, c1, c2),
        "problema":    _sv_problema(c1),
        "consecuencia":_sv_consecuencia(c1),
        "solucion":    _sv_solucion(c1, c2),
        "beneficio":   _sv_beneficio(c1, c2),
        "cta":         _sv_cta(c1, c2),
        "contenido":   _sv_solucion(c1, c2),
    }


def _sv_portada(categoria: str, c1: str, c2: str) -> str:
    fn = _HEROES.get(categoria, _hero_tecnologia)
    svg = fn(c1, c2)
    return f'<div style="width:100%;height:120px;overflow:hidden;opacity:0.85">{svg}</div>'


def _sv_problema(c1: str) -> str:
    return f"""<div style="width:100%;padding:8px 0;display:flex;flex-direction:column;gap:5px">
  <div style="display:flex;align-items:center;gap:6px;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:6px;padding:6px 10px">
    <span style="font-size:16px;opacity:0.8">⚡</span>
    <div>
      <div style="font-size:8px;font-weight:700;color:#ef4444;letter-spacing:0.1em">PUNTO DE DOLOR</div>
      <div style="font-size:9px;color:rgba(255,255,255,0.6);margin-top:1px">Problema identificado</div>
    </div>
  </div>
  <div style="display:flex;gap:4px">
    <div style="flex:1;background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);border-radius:5px;padding:5px 8px">
      <div style="font-size:8px;color:#f87171;font-weight:600">✗ Costo alto</div>
    </div>
    <div style="flex:1;background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);border-radius:5px;padding:5px 8px">
      <div style="font-size:8px;color:#f87171;font-weight:600">✗ Baja eficiencia</div>
    </div>
  </div>
</div>"""


def _sv_consecuencia(c1: str) -> str:
    return f"""<div style="width:100%;padding:6px 0;display:flex;flex-direction:column;gap:5px">
  <div style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);border-radius:6px;padding:6px 10px;display:flex;align-items:center;gap:6px">
    <span style="font-size:16px">⚠️</span>
    <div style="font-size:8px;font-weight:700;color:#f59e0b;letter-spacing:0.1em">IMPACTO REAL</div>
  </div>
  <div style="background:rgba(239,68,68,0.06);border-radius:5px;padding:5px 8px">
    <div style="font-size:8px;color:#fca5a5;line-height:1.4">Cada mes sin solución = recursos perdidos y competidores ganando terreno</div>
  </div>
  <div style="font-size:8px;font-weight:700;letter-spacing:0.1em;border:1px solid rgba(251,191,36,0.4);color:#f59e0b;border-radius:4px;padding:3px 8px;display:inline-block">EL COSTO DE NO ACTUAR</div>
</div>"""


def _sv_solucion(c1: str, c2: str) -> str:
    return f"""<div style="width:100%;padding:6px 0;display:flex;flex-direction:column;gap:5px">
  <div style="background:{c1}14;border:1px solid {c1}44;border-radius:6px;padding:6px 10px;display:flex;align-items:center;gap:6px">
    <span style="font-size:16px;opacity:0.85">💡</span>
    <div>
      <div style="font-size:8px;font-weight:700;color:{c1};letter-spacing:0.1em">SOLUCIÓN PROBADA</div>
      <div style="font-size:9px;color:rgba(255,255,255,0.55);margin-top:1px">Implementación comprobada</div>
    </div>
  </div>
  <div style="display:flex;gap:4px">
    <div style="flex:1;background:{c1}10;border:1px solid {c1}30;border-radius:5px;padding:5px 8px">
      <div style="font-size:8px;color:{c1};font-weight:600">✓ Eficiente</div>
    </div>
    <div style="flex:1;background:{c2}10;border:1px solid {c2}30;border-radius:5px;padding:5px 8px">
      <div style="font-size:8px;color:{c2};font-weight:600">✓ Escalable</div>
    </div>
  </div>
</div>"""


def _sv_beneficio(c1: str, c2: str) -> str:
    return f"""<div style="width:100%;padding:6px 0;display:flex;flex-direction:column;gap:5px">
  <div style="display:flex;gap:5px">
    <div style="flex:1;background:{c1}18;border:1px solid {c1}44;border-radius:7px;padding:8px;text-align:center">
      <div style="font-size:16px;font-weight:900;color:{c1};line-height:1">+40%</div>
      <div style="font-size:7px;color:rgba(255,255,255,0.4);margin-top:2px">Eficiencia</div>
    </div>
    <div style="flex:1;background:{c2}14;border:1px solid {c2}3a;border-radius:7px;padding:8px;text-align:center">
      <div style="font-size:16px;font-weight:900;color:{c2};line-height:1">3x</div>
      <div style="font-size:7px;color:rgba(255,255,255,0.4);margin-top:2px">Productividad</div>
    </div>
    <div style="flex:1;background:{c1}10;border:1px solid {c1}2a;border-radius:7px;padding:8px;text-align:center">
      <div style="font-size:16px;font-weight:900;color:{c1};line-height:1;opacity:0.8">-60%</div>
      <div style="font-size:7px;color:rgba(255,255,255,0.35);margin-top:2px">Costos</div>
    </div>
  </div>
  <div style="box-shadow:0 0 12px {c1}44;background:{c1}14;border:1px solid {c1}55;color:{c1};font-size:8px;font-weight:700;letter-spacing:0.1em;border-radius:4px;padding:3px 9px;display:inline-block">RESULTADOS COMPROBADOS</div>
</div>"""


def _sv_cta(c1: str, c2: str) -> str:
    return f"""<div style="width:100%;padding:6px 0;display:flex;flex-direction:column;gap:8px;align-items:center">
  <div style="background:linear-gradient(90deg,{c1},{c2});border-radius:20px;padding:9px 22px;font-size:11px;font-weight:700;color:#fff;box-shadow:0 4px 16px {c1}44;text-align:center">Hablar con un experto →</div>
  <div style="font-size:9px;color:rgba(255,255,255,0.4)">🔗 Link en bio · Respuesta en 24h</div>
</div>"""
