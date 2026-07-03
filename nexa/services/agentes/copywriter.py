"""
Agente Copywriter — Nexa AI
Genera contenido de marketing auténtico, diferenciado por tipo y tono de marca.

Usa Claude API (claude-haiku-4-5) cuando ANTHROPIC_API_KEY está configurada.
Si no hay clave o falla la llamada, cae al generador algorítmico interno.
"""

import json
import logging
import os
import random

logger = logging.getLogger("nexa.copywriter")

# ── Integración Claude AI ─────────────────────────────────────────────────────

try:
    import anthropic as _anthropic_sdk
    _HAS_ANTHROPIC = True
except ImportError:
    _HAS_ANTHROPIC = False

_MODELO = os.environ.get("NEXA_COPYWRITER_MODEL", "claude-haiku-4-5")
_SISTEMA = (
    "Eres un copywriter especialista en Instagram para PYMEs latinoamericanas.\n"
    "Tu misión: crear contenido que detenga el scroll, genere engagement real y convierta seguidores en clientes.\n\n"
    "REGLAS ABSOLUTAS:\n"
    "- CERO frases genéricas: nunca digas 'potencia tu negocio', 'soluciones integrales', "
    "'lleva tu empresa al siguiente nivel', 'en un mundo cada vez más digitalizado', 'apasionados por'.\n"
    "- Sé específico y concreto: nombra el dolor real, el resultado real, la solución real.\n"
    "- Tono auténtico LATAM: directo, cercano, sin artificialidad corporativa.\n"
    "- El hook debe ser imposible de ignorar: pregunta que duele, dato inesperado, o afirmación contraintuitiva.\n"
    "- Adapta el vocabulario al rubro exacto — no hables de 'empresa' o 'negocio' cuando puedes decir "
    "'veterinaria', 'estudio', 'taller', o lo que corresponda.\n"
    "- Responde SIEMPRE con JSON válido, sin texto adicional, sin bloques markdown."
)


def _cliente_claude():
    if not _HAS_ANTHROPIC:
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None
    return _anthropic_sdk.Anthropic(api_key=api_key)


def _llamar_claude(prompt_usuario: str) -> dict | None:
    """Llama a Claude y retorna el JSON parseado, o None si falla."""
    cliente = _cliente_claude()
    if not cliente:
        return None
    try:
        respuesta = cliente.messages.create(
            model=_MODELO,
            max_tokens=1024,
            system=_SISTEMA,
            messages=[{"role": "user", "content": prompt_usuario}],
        )
        texto = respuesta.content[0].text.strip()
        if texto.startswith("```"):
            lineas = texto.split("\n")
            texto = "\n".join(lineas[1:-1] if lineas[-1].strip() == "```" else lineas[1:])
        return json.loads(texto)
    except Exception as exc:
        logger.warning("Claude copywriter error (%s): %s — fallback algorítmico", _MODELO, exc)
        return None


# ── Prompts por formato ────────────────────────────────────────────────────────

def _prompt_post(ctx: dict) -> str:
    partes = [
        f"EMPRESA: {ctx['nombre']} | RUBRO: {ctx['rubro']}",
        f"TONO: {ctx['tono']} | PILAR: {ctx['pilar']}",
        f"TEMA: {ctx['tema']}",
        f"Propuesta de valor: {ctx['propuesta']}",
        f"Público objetivo: {ctx['publico']}",
        f"Servicios: {ctx['servicios'][:150]}",
    ]
    if ctx.get("resumen"):
        partes.append(f"Contexto de marca: {ctx['resumen'][:200]}")
    if ctx.get("estilo"):
        partes.append(f"Estilo de comunicación: {ctx['estilo']}")
    if ctx.get("palabras"):
        partes.append(f"Palabras clave de la marca: {', '.join(ctx['palabras'][:4])}")
    if ctx["instrucciones"]:
        partes.append(f"Instrucciones especiales: {ctx['instrucciones']}")
    if ctx["evitar"]:
        partes.append(f"NUNCA mencionar: {ctx['evitar']}")
    partes += [
        "",
        "Genera un post de Instagram que detenga el scroll.",
        "HOOK: pregunta que duele, dato inesperado, o afirmación contraintuitiva — máx. 2 líneas.",
        "BENEFICIO: resultado concreto que obtiene el cliente — qué cambia en su día a día (no promesas vagas).",
        "PRUEBA: dato real, caso o especificidad que genera credibilidad — nunca inventes estadísticas.",
        "CTA: acción concreta y simple — no 'visita nuestro sitio', sino algo que el usuario pueda hacer ahora.",
        'Retorna SOLO este JSON: {"titulo":"...","hook":"...","beneficio":"...","prueba":"...","cta":"..."}',
        "Límites: titulo≤80, hook≤120, beneficio≤160, prueba≤130, cta≤90 chars.",
    ]
    return "\n".join(partes)


def _prompt_carrusel(ctx: dict) -> str:
    partes = [
        f"EMPRESA: {ctx['nombre']} | RUBRO: {ctx['rubro']}",
        f"TONO: {ctx['tono']} | PILAR: {ctx['pilar']}",
        f"TEMA: {ctx['tema']}",
        f"Propuesta de valor: {ctx['propuesta']}",
        f"Público objetivo: {ctx['publico']}",
        f"Servicios: {ctx['servicios'][:150]}",
    ]
    if ctx.get("resumen"):
        partes.append(f"Contexto de marca: {ctx['resumen'][:200]}")
    if ctx.get("estilo"):
        partes.append(f"Estilo de comunicación: {ctx['estilo']}")
    if ctx.get("palabras"):
        partes.append(f"Palabras clave de la marca: {', '.join(ctx['palabras'][:4])}")
    if ctx["instrucciones"]:
        partes.append(f"Instrucciones especiales: {ctx['instrucciones']}")
    if ctx["evitar"]:
        partes.append(f"NUNCA mencionar: {ctx['evitar']}")
    partes += [
        "",
        "Genera un carrusel de Instagram de 6 slides. Cada slide debe funcionar como titular independiente — alguien que lo vea solo debe entender de qué trata.",
        "- Slide 1 (portada): titular que obligue a deslizar — promesa clara o pregunta poderosa",
        "- Slide 2 (problema): el dolor específico que el público reconoce al instante",
        "- Slide 3 (consecuencia): qué le cuesta ignorar este problema — el costo real",
        "- Slide 4 (solucion): cómo lo resuelve esta empresa — concreto, no genérico",
        "- Slide 5 (beneficio): el resultado en la vida del cliente después de trabajar con ellos",
        "- Slide 6 (cta): una sola acción, simple y directa — qué hace el usuario ahora mismo",
        'Retorna SOLO este JSON: {"titulo":"...","copy_intro":"...","cta_principal":"...","slides":[{"numero":1,"tipo":"portada","texto":"...","subtexto":"..."},{"numero":2,"tipo":"problema","texto":"..."},{"numero":3,"tipo":"consecuencia","texto":"..."},{"numero":4,"tipo":"solucion","texto":"..."},{"numero":5,"tipo":"beneficio","texto":"..."},{"numero":6,"tipo":"cta","texto":"..."}]}',
        "Límites: titulo≤80, copy_intro≤200, cta_principal≤80, texto de cada slide≤90 chars.",
    ]
    return "\n".join(partes)


def _prompt_historia(ctx: dict) -> str:
    partes = [
        f"EMPRESA: {ctx['nombre']} | RUBRO: {ctx['rubro']}",
        f"TONO: {ctx['tono']} | PILAR: {ctx['pilar']}",
        f"TEMA: {ctx['tema']}",
        f"Propuesta de valor: {ctx['propuesta']}",
        f"Público objetivo: {ctx['publico']}",
        f"Servicios: {ctx['servicios'][:120]}",
    ]
    if ctx.get("resumen"):
        partes.append(f"Contexto de marca: {ctx['resumen'][:150]}")
    if ctx.get("estilo"):
        partes.append(f"Estilo de comunicación: {ctx['estilo']}")
    if ctx["instrucciones"]:
        partes.append(f"Instrucciones especiales: {ctx['instrucciones']}")
    if ctx["evitar"]:
        partes.append(f"NUNCA mencionar: {ctx['evitar']}")
    partes += [
        "",
        "Genera una Historia de Instagram (3 pantallas). Deben leerse como una historia rápida, no como un anuncio.",
        "- Pantalla 1 (problema): pregunta o situación que el público reconoce al instante — máx. 2 líneas, lenguaje coloquial",
        "- Pantalla 2 (consecuencia): el costo emocional o económico de no resolverlo — específico, no abstracto",
        "- Pantalla 3 (solucion): la salida que ofrece la empresa, con CTA directo al link en bio",
        'Retorna SOLO este JSON: {"titulo":"...","copy_corto":"...","pantallas":[{"numero":1,"duracion":"7s","rol":"problema","texto":"...","subtexto":"¿Te ha pasado? 👇","sticker":"encuesta"},{"numero":2,"duracion":"7s","rol":"consecuencia","texto":"...","subtexto":"El costo de no actuar","sticker":"deslizador"},{"numero":3,"duracion":"6s","rol":"solucion","texto":"...","subtexto":"...","sticker":"link"}]}',
        "Límites: titulo≤60, copy_corto≤80, texto de cada pantalla≤75 chars.",
    ]
    return "\n".join(partes)


def _prompt_reel(ctx: dict) -> str:
    partes = [
        f"EMPRESA: {ctx['nombre']} | RUBRO: {ctx['rubro']}",
        f"TONO: {ctx['tono']} | PILAR: {ctx['pilar']}",
        f"TEMA: {ctx['tema']}",
        f"Propuesta de valor: {ctx['propuesta']}",
        f"Público objetivo: {ctx['publico']}",
        f"Servicios: {ctx['servicios'][:120]}",
    ]
    if ctx.get("resumen"):
        partes.append(f"Contexto de marca: {ctx['resumen'][:150]}")
    if ctx.get("estilo"):
        partes.append(f"Estilo de comunicación: {ctx['estilo']}")
    if ctx["instrucciones"]:
        partes.append(f"Instrucciones especiales: {ctx['instrucciones']}")
    if ctx["evitar"]:
        partes.append(f"NUNCA mencionar: {ctx['evitar']}")
    partes += [
        "",
        "Genera un Reel de Instagram (5 escenas, 30s). Escribe para quien lo ve EN MOVIMIENTO, no para quien lo lee.",
        "- texto: narración o voz en off (puede ser más largo, descripción completa de lo que se dice)",
        "- texto_pantalla: texto que aparece sobre el video — MUY CORTO, 3-5 palabras máximo, impacto visual inmediato",
        "ESTRUCTURA:",
        "- Escena 1 hook (0-5s): primera frase que impide hacer scroll — dato, pregunta o afirmación disruptiva",
        "- Escena 2 problema (5-10s): el dolor que reconocen en 5 segundos, lenguaje cotidiano",
        "- Escena 3 solucion (10-20s): cómo lo resuelves — nombra la empresa, sé específico",
        "- Escena 4 beneficio (20-25s): el resultado en la vida del cliente, no lo que hace la empresa",
        "- Escena 5 cta (25-30s): una sola acción — seguir, escribir, o ir al link",
        'Retorna SOLO este JSON: {"titulo":"...","copy":"...","escenas":[{"numero":1,"tipo":"hook","rango":"0-5s","duracion_seg":5,"texto":"...","texto_pantalla":"...","transicion":"corte"},{"numero":2,"tipo":"problema","rango":"5-10s","duracion_seg":5,"texto":"...","texto_pantalla":"...","transicion":"fundido"},{"numero":3,"tipo":"solucion","rango":"10-20s","duracion_seg":10,"texto":"...","texto_pantalla":"...","transicion":"corte"},{"numero":4,"tipo":"beneficio","rango":"20-25s","duracion_seg":5,"texto":"...","texto_pantalla":"...","transicion":"fundido"},{"numero":5,"tipo":"cta","rango":"25-30s","duracion_seg":5,"texto":"...","texto_pantalla":"...","transicion":"corte"}]}',
        "Límites: titulo≤60, copy≤200, texto≤120, texto_pantalla≤35 chars.",
    ]
    return "\n".join(partes)


# ── Ensambladores: Claude JSON → formato interno ──────────────────────────────

def _ensamblar_post(ctx: dict, ia: dict) -> dict:
    hook      = ia.get("hook", "")
    beneficio = ia.get("beneficio", "")
    prueba    = ia.get("prueba", "")
    cta       = ia.get("cta", "")
    titulo    = ia.get("titulo") or ctx["tema"][:80]
    copy      = "\n\n".join(p for p in [hook, beneficio, prueba, cta] if p)
    return {
        "titulo": titulo,
        "copy":   copy,
        "hashtags": _hashtags(ctx, tipo="post"),
        "cta":    cta,
        "estructura_json": {
            "formato": "post",
            "pilar":   ctx["pilar"],
            "ia_generado": True,
            "secciones": [
                {"tipo": "hook",      "texto": hook},
                {"tipo": "beneficio", "texto": beneficio},
                {"tipo": "prueba",    "texto": prueba},
                {"tipo": "cta",       "texto": cta},
            ],
        },
    }


def _ensamblar_carrusel(ctx: dict, ia: dict) -> dict:
    slides_ia = ia.get("slides", [])
    tipos     = ["portada", "problema", "consecuencia", "solucion", "beneficio", "cta"]
    slides    = []
    for i, tipo in enumerate(tipos, 1):
        s     = next((x for x in slides_ia if x.get("tipo") == tipo), {})
        entry = {"numero": i, "tipo": tipo, "texto": s.get("texto", f"[{tipo}]")}
        if tipo == "portada":
            entry["subtexto"] = s.get("subtexto", f"Por {ctx['nombre']}")
        slides.append(entry)
    titulo = ia.get("titulo") or f"{ctx['tema'][:70]} [Carrusel]"
    return {
        "titulo":   titulo,
        "copy":     ia.get("copy_intro", ""),
        "hashtags": _hashtags(ctx, tipo="carrusel"),
        "cta":      ia.get("cta_principal", ""),
        "estructura_json": {
            "formato": "carrusel",
            "ia_generado": True,
            "diapositivas": slides,
        },
    }


def _ensamblar_historia(ctx: dict, ia: dict) -> dict:
    pantallas_ia = ia.get("pantallas", [])
    config       = [("problema", "7s", "encuesta"), ("consecuencia", "7s", "deslizador"), ("solucion", "6s", "link")]
    pantallas    = []
    for i, (rol, dur, sticker) in enumerate(config, 1):
        p = next((x for x in pantallas_ia if x.get("rol") == rol), {})
        pantallas.append({
            "numero": i, "duracion": dur, "rol": rol,
            "texto":    p.get("texto", ""),
            "subtexto": p.get("subtexto", ""),
            "sticker":  sticker,
        })
    titulo = ia.get("titulo") or f"Historia: {ctx['tema'][:60]}"
    return {
        "titulo":   titulo,
        "copy":     ia.get("copy_corto", ""),
        "hashtags": _hashtags(ctx, tipo="historia"),
        "cta":      "Ver más → Link en bio",
        "estructura_json": {"formato": "historia", "ia_generado": True, "pantallas": pantallas},
    }


def _ensamblar_reel(ctx: dict, ia: dict) -> dict:
    escenas_ia = ia.get("escenas", [])
    config     = [
        ("hook",      "0-5s",   5,  "corte"),
        ("problema",  "5-10s",  5,  "fundido"),
        ("solucion",  "10-20s", 10, "corte"),
        ("beneficio", "20-25s", 5,  "fundido"),
        ("cta",       "25-30s", 5,  "corte"),
    ]
    escenas = []
    for i, (tipo, rango, dur, trans) in enumerate(config, 1):
        e     = next((x for x in escenas_ia if x.get("tipo") == tipo), {})
        texto = e.get("texto", "")
        escenas.append({
            "numero": i, "tipo": tipo, "rango": rango, "duracion_seg": dur,
            "texto":          texto,
            "texto_pantalla": e.get("texto_pantalla") or texto[:60],
            "transicion":     trans,
        })
    titulo = ia.get("titulo") or f"Reel: {ctx['tema'][:60]}"
    return {
        "titulo":   titulo,
        "copy":     ia.get("copy", ""),
        "hashtags": _hashtags(ctx, tipo="reel"),
        "cta":      _cta_principal(ctx),
        "estructura_json": {
            "formato":            "reel",
            "duracion":           "30s",
            "duracion_total_seg": 30,
            "hook":               escenas[0]["texto"] if escenas else "",
            "ia_generado":        True,
            "escenas":            escenas,
        },
    }


# ── API pública ───────────────────────────────────────────────────────────────

def generar_contenido_completo(
    empresa,
    memoria_marca,
    tipo_contenido: str,
    pilar: str,
    objetivo: str,
    semana: int = 1,
    tema: str = None,
    enfoque: str = None,
) -> dict:
    """
    Genera una pieza de contenido completa lista para publicar.
    - pilar: categoría temática (ej. "Automatización")
    - tema: asunto específico del brief (ej. "5 tareas que puedes automatizar hoy")
    - enfoque: ángulo o propósito de la pieza
    Retorna: titulo, copy, hashtags, cta, estructura_json.
    """
    ctx = _contexto(empresa, memoria_marca, pilar, objetivo, semana, tema, enfoque)
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

def _contexto(empresa, memoria_marca, pilar: str, objetivo: str, semana: int,
              tema: str = None, enfoque: str = None) -> dict:
    m = memoria_marca
    return {
        "nombre":        empresa.nombre_empresa,
        "rubro":         empresa.rubro,
        "tono":          empresa.tono_marca,
        "pilar":         pilar,
        "tema":          (tema or pilar).strip(),
        "enfoque":       (enfoque or "").strip(),
        "objetivo":      objetivo,
        "semana":        semana,
        "publico":       empresa.publico_objetivo,
        "propuesta":     (m.propuesta_valor if m else empresa.descripcion[:200]).strip(),
        "servicios":     (m.servicios_principales if m else empresa.rubro).strip(),
        "palabras":      ([p.strip() for p in m.palabras_clave.split(",") if p.strip()][:5]
                         if m and m.palabras_clave else []),
        "estilo":        (m.estilo_comunicacion if m else "").strip(),
        "instrucciones": (m.instrucciones_ia if m else "").strip(),
        "resumen":       (m.resumen_marca if m else "").strip(),
        "evitar":        (m.evitar_mencionar if m else "").strip(),
        "slug":          empresa.nombre_empresa.replace(" ", ""),
    }


# ── CARRUSEL ──────────────────────────────────────────────────────────────────

def _generar_carrusel(ctx: dict) -> dict:
    ia = _llamar_claude(_prompt_carrusel(ctx))
    if ia:
        return _ensamblar_carrusel(ctx, ia)

    # ── fallback algorítmico ──
    nombre    = ctx["nombre"]
    pilar     = ctx["pilar"]
    tema      = ctx["tema"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    publico   = ctx["publico"]

    hook         = tema if len(tema) > 20 else _hook_carrusel(pilar, nombre, propuesta)
    titulo       = f"{hook} [Carrusel]"
    problema     = _problema(pilar, publico)
    consecuencia = _consecuencia_slide(pilar, publico)
    solucion     = _solucion_slide(pilar, propuesta, servicios, nombre)
    beneficio    = _beneficio(pilar, servicios[:130], nombre)
    cta_sl       = _cta_slide(ctx["tono"], nombre, pilar)

    copy = (
        f"{hook}\n\n"
        f"Si eres {_publico_corto(publico)}, este carrusel es para ti 👇\n\n"
        f"Desliza para descubrir cómo {nombre} puede ayudarte."
    )

    slides = [
        {"numero": 1, "tipo": "portada",     "texto": hook,        "subtexto": f"Por {nombre}"},
        {"numero": 2, "tipo": "problema",    "texto": problema},
        {"numero": 3, "tipo": "consecuencia","texto": consecuencia},
        {"numero": 4, "tipo": "solucion",    "texto": solucion},
        {"numero": 5, "tipo": "beneficio",   "texto": beneficio},
        {"numero": 6, "tipo": "cta",         "texto": cta_sl},
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
    ia = _llamar_claude(_prompt_post(ctx))
    if ia:
        return _ensamblar_post(ctx, ia)

    # ── fallback algorítmico ──
    nombre    = ctx["nombre"]
    pilar     = ctx["pilar"]
    tema      = ctx["tema"]
    enfoque   = ctx["enfoque"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    tono      = ctx["tono"]

    hook      = tema if len(tema) > 20 else _gancho_post(pilar, nombre, tono)
    titulo    = tema[:80] if len(tema) > 20 else f"{pilar}: {_titular_post(pilar, nombre)}"
    beneficio = enfoque if enfoque else propuesta[:130]
    prueba    = _prueba_post(pilar, servicios, nombre)
    cta_copy  = _cta_principal(ctx)

    copy = "\n\n".join([hook, beneficio, prueba, cta_copy])

    return {
        "titulo":    titulo,
        "copy":      copy,
        "hashtags":  _hashtags(ctx, tipo="post"),
        "cta":       cta_copy,
        "estructura_json": {
            "formato": "post",
            "pilar":   pilar,
            "secciones": [
                {"tipo": "hook",      "texto": hook},
                {"tipo": "beneficio", "texto": beneficio},
                {"tipo": "prueba",    "texto": prueba},
                {"tipo": "cta",       "texto": cta_copy},
            ],
        },
    }


# ── HISTORIA ──────────────────────────────────────────────────────────────────

def _generar_historia(ctx: dict) -> dict:
    ia = _llamar_claude(_prompt_historia(ctx))
    if ia:
        return _ensamblar_historia(ctx, ia)

    # ── fallback algorítmico ──
    nombre    = ctx["nombre"]
    pilar     = ctx["pilar"]
    tema      = ctx["tema"]
    propuesta = ctx["propuesta"]
    publico   = ctx["publico"]
    tono      = ctx["tono"]

    problema_txt     = tema[:70] if len(tema) > 20 else _texto_problema_historia(pilar, publico)
    consecuencia_txt = _consecuencia_historia(pilar, nombre, publico)
    solucion_txt     = propuesta[:80]
    cta_txt          = _cta_historia(tono)

    titulo = f"Historia: {tema[:60]}" if len(tema) > 20 else f"Historia: {pilar}"

    pantallas = [
        {
            "numero":   1, "duracion": "7s", "rol": "problema",
            "texto":    problema_txt,
            "subtexto": "¿Te ha pasado? 👇",
            "sticker":  "encuesta",
        },
        {
            "numero":   2, "duracion": "7s", "rol": "consecuencia",
            "texto":    consecuencia_txt,
            "subtexto": "El costo de no actuar",
            "sticker":  "deslizador",
        },
        {
            "numero":   3, "duracion": "6s", "rol": "solucion",
            "texto":    f"{nombre}: {solucion_txt}",
            "subtexto": cta_txt,
            "sticker":  "link",
        },
    ]

    texto_corto = f"{problema_txt[:60].rstrip('.')} → {nombre} tiene la solución."

    return {
        "titulo":    titulo,
        "copy":      texto_corto,
        "hashtags":  _hashtags(ctx, tipo="historia"),
        "cta":       "Ver más → Link en bio",
        "estructura_json": {"formato": "historia", "pantallas": pantallas},
    }


# ── REEL ──────────────────────────────────────────────────────────────────────

def _generar_reel(ctx: dict) -> dict:
    ia = _llamar_claude(_prompt_reel(ctx))
    if ia:
        return _ensamblar_reel(ctx, ia)

    # ── fallback algorítmico ──
    nombre    = ctx["nombre"]
    pilar     = ctx["pilar"]
    tema      = ctx["tema"]
    propuesta = ctx["propuesta"]
    servicios = ctx["servicios"]
    tono      = ctx["tono"]
    publico   = ctx["publico"]

    hook       = tema if len(tema) > 20 else _hook_reel(pilar, nombre)
    problema   = _problema_reel(pilar, publico)
    solucion   = _solucion_reel(pilar, propuesta[:80], nombre)
    beneficio  = _beneficio_reel(pilar, servicios[:80], nombre)
    cta_texto  = _cta_reel(tono, nombre)
    titulo     = f"Reel: {hook[:60]}"

    escenas = [
        {
            "numero": 1, "tipo": "hook",
            "rango": "0-5s", "duracion_seg": 5,
            "texto": hook,
            "texto_pantalla": hook[:60],
            "transicion": "corte",
        },
        {
            "numero": 2, "tipo": "problema",
            "rango": "5-10s", "duracion_seg": 5,
            "texto": problema,
            "texto_pantalla": problema[:60],
            "transicion": "fundido",
        },
        {
            "numero": 3, "tipo": "solucion",
            "rango": "10-20s", "duracion_seg": 10,
            "texto": solucion,
            "texto_pantalla": solucion[:60],
            "transicion": "corte",
        },
        {
            "numero": 4, "tipo": "beneficio",
            "rango": "20-25s", "duracion_seg": 5,
            "texto": beneficio,
            "texto_pantalla": beneficio[:60],
            "transicion": "fundido",
        },
        {
            "numero": 5, "tipo": "cta",
            "rango": "25-30s", "duracion_seg": 5,
            "texto": cta_texto,
            "texto_pantalla": cta_texto[:60],
            "transicion": "corte",
        },
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
            "formato":           "reel",
            "duracion":          "30s",
            "duracion_total_seg": 30,
            "hook":              hook,
            "escenas":           escenas,
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

def _prueba_post(pilar: str, servicios: str, nombre: str) -> str:
    pilar_l = pilar.lower()
    opciones = [
        f"Dato: las empresas que implementan {pilar_l} reportan hasta un 40% más de eficiencia operativa.",
        f"No es teoría: en {nombre} ya lo hacemos con {servicios[:60].lower().rstrip('.')}.",
        f"Resultado comprobado: {servicios[:70].lower().rstrip('.')} — menos tiempo, más resultados.",
    ]
    return random.choice(opciones)


def _texto_problema_historia(pilar: str, publico: str) -> str:
    pilar_l = pilar.lower()
    return (
        f"¿Sigues gestionando {pilar_l} de forma manual? "
        f"Para {_publico_corto(publico)}, eso significa horas perdidas cada semana."
    )


def _consecuencia_historia(pilar: str, nombre: str, publico: str) -> str:
    pilar_l = pilar.lower()
    return (
        f"Sin {pilar_l} bien implementado, las empresas asumen costos innecesarios "
        f"y pierden competitividad frente a quienes ya lo aplican."
    )


def _consecuencia_slide(pilar: str, publico: str) -> str:
    pilar_l = pilar.lower()
    return (
        f"Sin {pilar_l}, tu empresa pierde tiempo, aumenta costos y cede terreno "
        f"a competidores que ya tomaron acción."
    )


def _solucion_slide(pilar: str, propuesta: str, servicios: str, nombre: str) -> str:
    svc = servicios[:80].lower().rstrip(".")
    prop = propuesta[:60].rstrip(".")
    return f"{nombre} resuelve esto con {svc}. {prop}."


def _problema_reel(pilar: str, publico: str) -> str:
    pilar_l = pilar.lower()
    return (
        f"¿Sabías que {_publico_corto(publico)} pierde horas semanales "
        f"por no tener {pilar_l} bien implementado?"
    )


def _solucion_reel(pilar: str, propuesta: str, nombre: str) -> str:
    prop = propuesta.rstrip(".")
    return f"{nombre} lo soluciona: {prop}."


def _beneficio_reel(pilar: str, servicios: str, nombre: str) -> str:
    svc = servicios[:60].lower().rstrip(".")
    return f"El resultado: {svc} — menos fricción, más resultados en menos tiempo."


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
