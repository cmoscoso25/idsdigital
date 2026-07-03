"""
Genera prompts de imagen optimizados para Flux Pro / DALL-E usando Claude.
Fallback algorítmico si Claude no está disponible.
"""
import os
import logging

logger = logging.getLogger("nexa.generador_prompts")

_SISTEMA = (
    "Eres un director creativo especialista en contenido visual para Instagram. "
    "Escribes prompts de generación de imágenes AI (Flux Pro) que producen resultados "
    "profesionales, modernos y coherentes con la marca. "
    "Reglas: siempre en inglés, muy descriptivo, sin mencionar texto ni letras en la imagen "
    "(el texto se superpone por separado), sin personas genéricas de stock. "
    "Responde SOLO con el prompt, sin explicaciones."
)


def _claude(peticion: str, max_tokens: int = 250) -> str | None:
    try:
        import anthropic as sdk
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None
        modelo = os.environ.get("NEXA_COPYWRITER_MODEL", "claude-haiku-4-5")
        cliente = sdk.Anthropic(api_key=api_key)
        resp = cliente.messages.create(
            model=modelo,
            max_tokens=max_tokens,
            system=_SISTEMA,
            messages=[{"role": "user", "content": peticion}],
        )
        return resp.content[0].text.strip()
    except Exception as exc:
        logger.warning("generador_prompts Claude error: %s", exc)
        return None


def generar_prompt_post(empresa, contenido, memoria_marca=None) -> str:
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    tema = contenido.titulo[:80]
    hook = ""
    if contenido.estructura_json:
        secciones = contenido.estructura_json.get("secciones", [])
        hook = next((s.get("texto", "") for s in secciones if s.get("tipo") == "hook"), "")
    propuesta = (memoria_marca.propuesta_valor[:100] if memoria_marca else empresa.descripcion[:100])

    peticion = (
        f"Instagram square post (1:1, 1080×1080px) para: {empresa.nombre_empresa} — {empresa.rubro}\n"
        f"Colores de marca: {color_p} (principal), {color_s} (acento)\n"
        f"Tema del post: {tema}\n"
        f"Mensaje central: {hook[:120] if hook else propuesta[:120]}\n\n"
        f"Genera un prompt Flux Pro que describa:\n"
        f"- Composición visual que refuerce '{tema}' sin ningún texto\n"
        f"- Ambiente profesional coherente con el rubro\n"
        f"- Colores {color_p} y {color_s} como dominantes\n"
        f"- Elementos abstractos, iconográficos o conceptuales (no personas de stock)\n"
        f"- Iluminación cinematográfica, estética premium B2B\n"
        f"Solo el prompt en inglés, máx. 180 palabras."
    )
    resultado = _claude(peticion)
    if resultado:
        return resultado

    return (
        f"Professional Instagram square post 1080x1080px for {empresa.nombre_empresa}, "
        f"{empresa.rubro} company. Gradient background {color_p} to {color_s}. "
        f"Abstract concept: {tema}. Minimalist premium B2B design, "
        f"no text, no stock people, cinematic lighting, ultra-sharp."
    )


def generar_prompt_historia(empresa, contenido, memoria_marca=None) -> str:
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    tema = contenido.titulo[:80]
    pantallas = contenido.estructura_json.get("pantallas", []) if contenido.estructura_json else []
    hook_pantalla = next((p.get("texto", "") for p in pantallas if p.get("rol") == "problema"), "")

    peticion = (
        f"Instagram Story (9:16, 1080×1920px) para: {empresa.nombre_empresa} — {empresa.rubro}\n"
        f"Colores: {color_p} y {color_s}\n"
        f"Tema: {tema}\n"
        f"Primer mensaje: {hook_pantalla[:100]}\n\n"
        f"Genera un prompt Flux Pro que describa:\n"
        f"- Composición vertical 9:16 que capture atención en 2 segundos\n"
        f"- Elemento visual central impactante relacionado con '{tema}'\n"
        f"- Zona superior e inferior despejadas para superponer texto\n"
        f"- Colores {color_p} y {color_s} dominantes\n"
        f"- Sin texto, sin personas genéricas\n"
        f"Solo el prompt en inglés, máx. 150 palabras."
    )
    resultado = _claude(peticion)
    if resultado:
        return resultado

    return (
        f"Professional Instagram Story 1080x1920px vertical 9:16 for {empresa.nombre_empresa}. "
        f"Vibrant gradient background {color_p} to {color_s}. "
        f"Central bold visual concept: {tema}. "
        f"Clean space top and bottom for text overlay. "
        f"Modern eye-catching design, no text, professional quality."
    )


def generar_prompt_carrusel(empresa, contenido, memoria_marca=None) -> str:
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    tema = contenido.titulo[:80]
    slides = contenido.estructura_json.get("diapositivas", []) if contenido.estructura_json else []
    problema = next((s.get("texto", "") for s in slides if s.get("tipo") == "problema"), "")
    solucion = next((s.get("texto", "") for s in slides if s.get("tipo") == "solucion"), "")

    peticion = (
        f"Instagram Carousel cover (1:1, 1080×1080px) para: {empresa.nombre_empresa} — {empresa.rubro}\n"
        f"Colores: {color_p} y {color_s}\n"
        f"Tema del carrusel: {tema}\n"
        f"Problema que aborda: {problema[:100]}\n"
        f"Solución que ofrece: {solucion[:100]}\n\n"
        f"Genera un prompt Flux Pro para la portada del carrusel que:\n"
        f"- Intrigue y motive a deslizar (swipe)\n"
        f"- Represente visualmente el tema sin texto\n"
        f"- Use los colores de marca como base\n"
        f"- Sea coherente con el rubro {empresa.rubro}\n"
        f"Solo el prompt en inglés, máx. 150 palabras."
    )
    resultado = _claude(peticion)
    if resultado:
        return resultado

    return (
        f"Professional Instagram carousel cover 1080x1080px for {empresa.nombre_empresa}. "
        f"Theme: {tema}. Brand colors {color_p} and {color_s}. "
        f"Compelling, swipe-inducing visual, no text, clean modern design."
    )


def generar_prompt_reel(empresa, contenido, memoria_marca=None) -> str:
    color_p = empresa.color_principal
    color_s = empresa.color_secundario
    tema = contenido.titulo[:80]
    escenas = contenido.estructura_json.get("escenas", []) if contenido.estructura_json else []
    hook_escena = next((e.get("texto", "") for e in escenas if e.get("tipo") == "hook"), "")

    peticion = (
        f"Instagram Reel thumbnail (9:16, 1080×1920px) para: {empresa.nombre_empresa} — {empresa.rubro}\n"
        f"Colores: {color_p} y {color_s}\n"
        f"Tema del reel: {tema}\n"
        f"Hook: {hook_escena[:120]}\n\n"
        f"Genera un prompt Flux Pro para el thumbnail del Reel que:\n"
        f"- Sea tan impactante que haga clic inevitable\n"
        f"- Transmita energía y movimiento (es un video)\n"
        f"- Composición vertical 9:16, sin texto\n"
        f"- Colores {color_p} y {color_s} dominantes\n"
        f"Solo el prompt en inglés, máx. 150 palabras."
    )
    resultado = _claude(peticion)
    if resultado:
        return resultado

    return (
        f"Dynamic Instagram Reel thumbnail 1080x1920px 9:16 for {empresa.nombre_empresa}. "
        f"High energy visual concept: {tema}. "
        f"Brand colors {color_p} and {color_s}. "
        f"Cinematic quality, no text, motion-suggesting composition."
    )
