"""
Agente Copywriter — Nexa AI
Genera contenido de marketing auténtico, diferenciado por tipo y tono de marca.

# === PUNTO DE CONEXIÓN API ===
# Para activar Claude/OpenAI, reemplazar `_generar_simulado` en cada función
# _copy_*. La firma de `generar_contenido_completo` no debe cambiar.
# === FIN PUNTO DE CONEXIÓN ===
"""

import random


def generar_contenido_completo(
    empresa,
    memoria_marca,
    tipo_contenido: str,
    pilar: str,
    objetivo: str,
    semana: int = 1,
) -> dict:
    """
    Genera una pieza de contenido completa lista para publicar.
    Retorna: titulo, copy, hashtags, cta, estructura_json.
    """
    ctx = _contexto(empresa, memoria_marca, pilar, objetivo, semana)
    generadores = {
        "carrusel": _generar_carrusel,
        "post":     _generar_post,
        "historia": _generar_historia,
        "reel":     _generar_reel,
        "campana":  _generar_campana,
    }
    fn = generadores.get(tipo_contenido, _generar_post)
    return fn(ctx)


def generar_copy(empresa, memoria_marca, tipo_contenido: str, tema: str, objetivo: str) -> dict:
    """Compatibilidad con la vista generar manual (empresa_detalle → generar)."""
    r = generar_contenido_completo(empresa, memoria_marca, tipo_contenido, tema, objetivo)
    return {"copy": r["copy"], "cta": r["cta"], "hashtags": r["hashtags"]}


# ── Contexto centralizado ──────────────────────────────────────────────────────

def _contexto(empresa, memoria_marca, pilar: str, objetivo: str, semana: int) -> dict:
    m = memoria_marca
    return {
        "nombre":      empresa.nombre_empresa,
        "rubro":       empresa.rubro,
        "tono":        empresa.tono_marca,
        "pilar":       pilar,
        "objetivo":    objetivo,
        "semana":      semana,
        "publico":     empresa.publico_objetivo,
        "propuesta":   (m.propuesta_valor if m else empresa.descripcion[:200]).strip(),
        "servicios":   (m.servicios_principales if m else empresa.rubro).strip(),
        "palabras":    ([p.strip() for p in m.palabras_clave.split(",") if p.strip()][:5]
                       if m and m.palabras_clave else []),
        "estilo":      (m.estilo_comunicacion if m else "").strip(),
        "instrucciones": (m.instrucciones_ia if m else "").strip(),
        "resumen":     (m.resumen_marca if m else "").strip(),
        "evitar":      (m.evitar_mencionar if m else "").strip(),
        "slug":        empresa.nombre_empresa.replace(" ", ""),
    }


# ── CARRUSEL ──────────────────────────────────────────────────────────────────

def _generar_carrusel(ctx: dict) -> dict:
    nombre   = ctx["nombre"]
    pilar    = ctx["pilar"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    publico  = ctx["publico"]

    hook = _hook_carrusel(pilar, nombre, propuesta)
    titulo = f"{hook} [Carrusel]"

    copy = (
        f"{hook}\n\n"
        f"Si eres {_publico_corto(publico)}, este carrusel es para ti 👇\n\n"
        f"Desliza para descubrir cómo {nombre} puede ayudarte con {pilar.lower()}."
    )

    slides = [
        {"numero": 1, "tipo": "portada",   "texto": hook, "subtexto": f"Por {nombre}"},
        {"numero": 2, "tipo": "problema",  "texto": _problema(pilar, publico)},
        {"numero": 3, "tipo": "contenido", "texto": propuesta[:130]},
        {"numero": 4, "tipo": "beneficio", "texto": _beneficio(pilar, servicios[:130], nombre)},
        {"numero": 5, "tipo": "cta",       "texto": _cta_slide(ctx["tono"], nombre, pilar)},
    ]

    return {
        "titulo":    titulo,
        "copy":      copy,
        "hashtags":  _hashtags(ctx, tipo="carrusel"),
        "cta":       _cta_principal(ctx),
        "estructura_json": {"formato": "carrusel", "diapositivas": slides},
    }


# ── POST ──────────────────────────────────────────────────────────────────────

def _generar_post(ctx: dict) -> dict:
    nombre   = ctx["nombre"]
    pilar    = ctx["pilar"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    publico  = ctx["publico"]
    tono     = ctx["tono"]

    gancho = _gancho_post(pilar, nombre, tono)
    titulo = f"{pilar}: {_titular_post(pilar, nombre)}"

    copy = "\n\n".join([
        gancho,
        propuesta[:150],
        f"En {nombre} trabajamos cada día para que {_publico_corto(publico)} pueda {_verbo_objetivo(ctx['objetivo'])} a través de {pilar.lower()}.",
        f"¿Quieres saber cómo? {_invitacion(tono)}",
    ])

    sugerencia = f"Imagen: {pilar} — fondo coherente con la identidad de {nombre}. Texto en overlay: \"{gancho[:60]}\""

    return {
        "titulo":    titulo,
        "copy":      copy,
        "hashtags":  _hashtags(ctx, tipo="post"),
        "cta":       _cta_principal(ctx),
        "estructura_json": {
            "formato": "imagen_unica",
            "sugerencia_visual": sugerencia,
            "pilar": pilar,
            "lineas_caption": 4,
        },
    }


# ── HISTORIA ──────────────────────────────────────────────────────────────────

def _generar_historia(ctx: dict) -> dict:
    nombre  = ctx["nombre"]
    pilar   = ctx["pilar"]
    propuesta = ctx["propuesta"]
    tono    = ctx["tono"]

    titulo = f"Historia: {pilar}"
    texto_corto = _texto_historia(pilar, propuesta, nombre)

    pantallas = [
        {
            "numero": 1, "duracion": "7s",
            "texto": f"💡 {pilar}",
            "subtexto": _frase_corta(pilar, propuesta),
            "sticker": _sticker(pilar),
        },
        {
            "numero": 2, "duracion": "7s",
            "texto": propuesta[:90],
            "subtexto": f"— {nombre}",
            "sticker": "deslizador",
        },
        {
            "numero": 3, "duracion": "6s",
            "texto": _cta_historia(tono),
            "subtexto": "🔗 Link en bio",
            "sticker": "link",
        },
    ]

    return {
        "titulo":    titulo,
        "copy":      texto_corto,
        "hashtags":  _hashtags(ctx, tipo="historia"),
        "cta":       "Ver más → Link en bio",
        "estructura_json": {"formato": "historia", "pantallas": pantallas},
    }


# ── REEL ──────────────────────────────────────────────────────────────────────

def _generar_reel(ctx: dict) -> dict:
    nombre   = ctx["nombre"]
    pilar    = ctx["pilar"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    tono     = ctx["tono"]

    hook = _hook_reel(pilar, nombre)
    titulo = f"Reel: {hook[:60]}"

    guion = [
        {"rango": "0-5s",  "texto": hook, "tipo": "hook"},
        {"rango": "5-15s", "texto": propuesta[:100], "tipo": "desarrollo"},
        {"rango": "15-25s","texto": _ejemplo_reel(pilar, servicios[:80], nombre), "tipo": "ejemplo"},
        {"rango": "25-30s","texto": _cta_reel(tono, nombre), "tipo": "cta"},
    ]

    copy = (
        f"{hook}\n\n"
        f"{propuesta[:120]}\n\n"
        f"🎬 Mira el video completo y descubre cómo {nombre} puede ayudarte."
    )

    return {
        "titulo":    titulo,
        "copy":      copy,
        "hashtags":  _hashtags(ctx, tipo="reel"),
        "cta":       _cta_principal(ctx),
        "estructura_json": {
            "formato": "reel",
            "duracion": "30s",
            "hook": hook,
            "escenas": guion,
        },
    }


# ── CAMPAÑA ───────────────────────────────────────────────────────────────────

def _generar_campana(ctx: dict) -> dict:
    nombre = ctx["nombre"]
    pilar  = ctx["pilar"]
    propuesta = ctx["propuesta"]

    titulo = f"Campaña: {pilar} con {nombre}"
    copy = (
        f"🚀 Lanzamos nuestra campaña sobre {pilar}.\n\n"
        f"{propuesta[:150]}\n\n"
        f"Durante los próximos días compartiremos contenido sobre {pilar.lower()} "
        f"diseñado especialmente para ti."
    )

    return {
        "titulo": titulo,
        "copy":   copy,
        "hashtags": _hashtags(ctx, tipo="campana"),
        "cta":    _cta_principal(ctx),
        "estructura_json": {
            "formato": "campana",
            "piezas": [
                {"tipo": "post",     "descripcion": f"Lanzamiento: ¿qué es {pilar}?"},
                {"tipo": "historia", "descripcion": "Encuesta: ¿conoces el tema?"},
                {"tipo": "carrusel", "descripcion": f"Guía de {pilar} en 5 pasos"},
                {"tipo": "reel",     "descripcion": f"Resumen de campaña {pilar}"},
            ],
        },
    }


# ── Helpers de copy ──────────────────────────────────────────────────────────

def _hook_carrusel(pilar: str, nombre: str, propuesta: str) -> str:
    pilar_l = pilar.lower()
    hooks = [
        f"¿Tu empresa todavía no usa {pilar_l}? Esto te interesa",
        f"{pilar}: la ventaja que separa a las empresas exitosas del resto",
        f"Lo que nadie te cuenta sobre {pilar_l} en los negocios",
        f"5 razones por las que {pilar_l} puede transformar tu empresa",
        f"Antes de ignorar {pilar_l}, lee esto",
    ]
    return random.choice(hooks)


def _gancho_post(pilar: str, nombre: str, tono: str) -> str:
    pilar_l = pilar.lower()
    ganchos = {
        "profesional": f"El {pilar_l} marca la diferencia entre crecer y estancarse.",
        "cercano":     f"¿Hablamos de {pilar_l}? Porque esto puede cambiar tu negocio. 💬",
        "inspirador":  f"✨ {pilar} no es una opción — es el camino.",
        "humoristico": f"😅 Seamos honestos: {pilar_l} suena complicado hasta que lo entiendes.",
        "exclusivo":   f"Las empresas que lideran el mercado tienen algo en común: {pilar_l}.",
        "educativo":   f"¿Sabes qué es realmente {pilar_l} y por qué importa para tu empresa?",
    }
    return ganchos.get(tono, f"{pilar}: todo lo que debes saber para crecer.")


def _titular_post(pilar: str, nombre: str) -> str:
    opciones = [
        f"por qué importa para tu empresa",
        f"cómo puede transformar tu negocio",
        f"lo que necesitas saber",
        f"la guía que necesitabas",
    ]
    return random.choice(opciones)


def _hook_reel(pilar: str, nombre: str) -> str:
    pilar_l = pilar.lower()
    hooks = [
        f"¿Sabías que {pilar_l} puede duplicar tu productividad? 🚀",
        f"3 errores que cometen las empresas con {pilar_l}",
        f"La verdad sobre {pilar_l} que nadie te dice",
        f"¿Cuánto te cuesta ignorar {pilar_l}?",
        f"Esto es lo que cambia cuando implementas {pilar_l}",
    ]
    return random.choice(hooks)


def _problema(pilar: str, publico: str) -> str:
    pilar_l = pilar.lower()
    return (
        f"Muchas empresas pierden tiempo y dinero por no aprovechar {pilar_l}. "
        f"¿Te identificas?"
    )


def _beneficio(pilar: str, servicios: str, nombre: str) -> str:
    return f"Con {nombre} puedes aplicar {pilar.lower()} de forma estratégica: {servicios[:100]}"


def _ejemplo_reel(pilar: str, servicios: str, nombre: str) -> str:
    return f"En {nombre} lo hacemos así: {servicios[:80]}"


def _texto_historia(pilar: str, propuesta: str, nombre: str) -> str:
    return f"{pilar} — {propuesta[:80]} Más info en el link 👇"


def _frase_corta(pilar: str, propuesta: str) -> str:
    return propuesta[:60].rstrip(".") + "..."


def _publico_corto(publico: str) -> str:
    if not publico:
        return "emprendedor o empresa"
    words = publico.split()
    return " ".join(words[:6]).lower().rstrip(",.")


def _verbo_objetivo(objetivo: str) -> str:
    obj_l = objetivo.lower()
    if "venta" in obj_l:     return "aumentar sus ventas"
    if "comunidad" in obj_l: return "construir su comunidad"
    if "reconoci" in obj_l:  return "posicionarse en el mercado"
    if "educa" in obj_l:     return "aprender y crecer"
    if "confian" in obj_l:   return "generar confianza en su mercado"
    return "alcanzar sus objetivos"


def _invitacion(tono: str) -> str:
    inv = {
        "profesional": "Escríbenos y conversemos.",
        "cercano":     "¡Escríbenos, estamos aquí para ayudarte! 👇",
        "inspirador":  "Da el primer paso hoy. 🌟",
        "humoristico": "¡No esperes más, escríbenos ya! 😄",
        "exclusivo":   "Solicita tu consulta →",
        "educativo":   "¿Preguntas? Escríbenos. 💡",
    }
    return inv.get(tono, "Contáctanos para saber más.")


def _sticker(pilar: str) -> str:
    pilar_l = pilar.lower()
    if any(w in pilar_l for w in ["pregunta", "encuesta", "mito", "sab"]):
        return "encuesta"
    if any(w in pilar_l for w in ["tip", "dato", "aprend", "guia"]):
        return "deslizador"
    return "encuesta"


def _cta_slide(tono: str, nombre: str, pilar: str) -> str:
    ctas = {
        "profesional": f"Contáctanos → {nombre}",
        "cercano":     f"¡Escríbenos hoy! 💬",
        "inspirador":  "Da el primer paso 🚀",
        "humoristico": "¡Hablemos! 😄",
        "exclusivo":   "Solicita tu consulta exclusiva →",
        "educativo":   "¿Dudas? Escríbenos 💡",
    }
    return ctas.get(tono, f"Contacta a {nombre}")


def _cta_historia(tono: str) -> str:
    ctas = {
        "profesional": "Más información →",
        "cercano":     "¡Cuéntanos qué piensas! 💬",
        "inspirador":  "✨ Más en nuestro perfil",
        "humoristico": "😄 Swipe up para más",
        "exclusivo":   "Acceso exclusivo →",
        "educativo":   "Aprende más 💡",
    }
    return ctas.get(tono, "Ver más →")


def _cta_reel(tono: str, nombre: str) -> str:
    ctas = {
        "profesional": f"Síguenos para más contenido de {nombre}",
        "cercano":     "Síguenos y únete a la comunidad 🤝",
        "inspirador":  "Síguenos para inspiración diaria ✨",
        "humoristico": "Síguenos, lo prometemos que vale la pena 😄",
        "exclusivo":   "Síguenos para contenido premium →",
        "educativo":   "Síguenos para más tips y guías 💡",
    }
    return ctas.get(tono, "Síguenos para más contenido")


def _cta_principal(ctx: dict) -> str:
    tono   = ctx["tono"]
    nombre = ctx["nombre"]
    pilar  = ctx["pilar"]
    obj    = ctx["objetivo"].lower()

    if "venta" in obj or "lead" in obj:
        base = f"¿Listo para dar el siguiente paso? Escríbenos y te ayudamos."
    elif "comunidad" in obj:
        base = f"Únete a nuestra comunidad y comparte este contenido."
    elif "educa" in obj:
        base = f"¿Quieres aprender más sobre {pilar.lower()}? Escríbenos."
    else:
        base = f"Contáctanos hoy y descubre cómo {nombre} puede ayudarte con {pilar.lower()}."

    emojis = {"cercano": " 💬", "inspirador": " 🚀", "educativo": " 💡"}
    return base + emojis.get(tono, "")


# ── Hashtags ──────────────────────────────────────────────────────────────────

_HASHTAGS_POR_PILAR = {
    "automatizacion":       ["#Automatizacion", "#Productividad", "#Eficiencia"],
    "inteligencia":         ["#InteligenciaArtificial", "#IA", "#Innovacion"],
    "ia":                   ["#InteligenciaArtificial", "#IA", "#Tecnologia"],
    "marketing":            ["#MarketingDigital", "#Estrategia", "#Contenido"],
    "equipo":               ["#Equipo", "#CulturaEmpresarial", "#Personas"],
    "historia":             ["#Historia", "#MarcaPersonal", "#Autenticidad"],
    "caso":                 ["#CasoDeExito", "#Resultados", "#Transformacion"],
    "ventas":               ["#Ventas", "#CrecimientoEmpresarial", "#Comercial"],
    "productividad":        ["#Productividad", "#Eficiencia", "#Optimizacion"],
    "transformacion":       ["#TransformacionDigital", "#Innovacion", "#Futuro"],
    "software":             ["#Software", "#Tecnologia", "#SolucionesTech"],
    "datos":                ["#BigData", "#Analitica", "#DecisionesBasadasEnDatos"],
    "comunidad":            ["#Comunidad", "#Conexion", "#Networking"],
    "educacion":            ["#Aprendizaje", "#Capacitacion", "#Conocimiento"],
    "tip":                  ["#Tips", "#Consejos", "#Aprendizaje"],
    "mito":                 ["#MitosYRealidades", "#Verdades", "#Educacion"],
}

_HASHTAGS_POR_OBJETIVO = {
    "ventas":        ["#Negocios", "#CrecimientoEmpresarial"],
    "reconocimiento":["#Marca", "#Posicionamiento"],
    "comunidad":     ["#Comunidad", "#Conexion"],
    "educacion":     ["#Aprendizaje", "#Tips"],
    "confianza":     ["#Confianza", "#Transparencia"],
}

_HASHTAGS_BASE = ["#Pymes", "#Emprendimiento", "#Chile"]


def _hashtags(ctx: dict, tipo: str) -> str:
    slug   = ctx["slug"]
    pilar  = ctx["pilar"].lower()
    tono   = ctx["tono"]
    rubro  = ctx["rubro"].split()[0].strip() if ctx["rubro"] else ""
    nombre_tag = f"#{slug}"

    pilar_tags = []
    for keyword, tags in _HASHTAGS_POR_PILAR.items():
        if keyword in pilar:
            pilar_tags.extend(tags)
            break

    objetivo_tags = _HASHTAGS_POR_OBJETIVO.get(ctx.get("objetivo", "")[:10].lower(), [])

    keyword_tags = []
    for kw in ctx.get("palabras", [])[:3]:
        tag = "#" + kw.replace(" ", "").capitalize()
        if len(tag) < 22 and tag not in keyword_tags:
            keyword_tags.append(tag)

    rubro_tag = f"#{rubro.capitalize()}" if rubro and len(rubro) > 2 else ""

    pool = ([nombre_tag]
            + pilar_tags[:2]
            + keyword_tags[:2]
            + objetivo_tags[:1]
            + _HASHTAGS_BASE[:2]
            + ([rubro_tag] if rubro_tag else []))

    seen, result = set(), []
    for tag in pool:
        t = tag.strip()
        if t and t.lower() not in seen and len(t) <= 24:
            seen.add(t.lower())
            result.append(t)
        if len(result) >= 8:
            break

    return " ".join(result)
