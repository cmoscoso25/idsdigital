"""
Servicio de generación de contenido para Nexa AI.

PUNTO DE CONEXIÓN API: cuando se active la integración con Claude/OpenAI,
reemplazar el cuerpo de `generar_contenido` con la llamada real a la API.
La firma y el dict de retorno no deben cambiar para no romper las vistas.
"""


def generar_contenido(
    empresa,
    memoria_marca,
    tipo_contenido: str,
    objetivo: str,
    tema: str,
) -> dict:
    """
    Genera contenido para Instagram/redes sociales.

    Retorna dict con: titulo, copy, hashtags, cta, estructura_json.

    # === REEMPLAZAR ESTE BLOQUE CON LLAMADA A API ===
    # Ejemplo futuro con Anthropic SDK:
    #
    # import anthropic
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-opus-4-8",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": _build_prompt(empresa, memoria_marca, tipo_contenido, objetivo, tema)}],
    # )
    # return _parse_response(message.content[0].text)
    # === FIN BLOQUE API ===
    """
    return _generar_simulado(empresa, memoria_marca, tipo_contenido, objetivo, tema)


def _generar_simulado(empresa, memoria_marca, tipo_contenido, objetivo, tema):
    nombre = empresa.nombre_empresa
    propuesta = memoria_marca.propuesta_valor if memoria_marca else f"expertos en {empresa.rubro}"
    servicios = memoria_marca.servicios_principales[:150] if memoria_marca else empresa.descripcion[:150]
    slug_nombre = nombre.replace(" ", "")
    slug_tema = tema.replace(" ", "")

    plantillas = {
        "carrusel": {
            "titulo": f"{nombre} — {tema}",
            "copy": (
                f"¿Sabías que {propuesta}?\n\n"
                f"Hoy te compartimos claves sobre {tema} para impulsar tu negocio. Desliza →"
            ),
            "hashtags": f"#{slug_nombre} #{slug_tema} #negocio #pyme #emprendimiento #marketing",
            "cta": "Guarda este carrusel y compártelo con quien lo necesite 📌",
            "estructura_json": {
                "formato": "carrusel",
                "diapositivas": [
                    {"numero": 1, "texto": f"¿Conoces {tema}?", "tipo": "portada"},
                    {"numero": 2, "texto": propuesta, "tipo": "contenido"},
                    {"numero": 3, "texto": servicios, "tipo": "contenido"},
                    {"numero": 4, "texto": f"Con {nombre} lo logramos", "tipo": "cierre"},
                    {"numero": 5, "texto": "Escríbenos hoy 👇", "tipo": "cta"},
                ],
            },
        },
        "historia": {
            "titulo": f"Historia: {tema} — {nombre}",
            "copy": f"💡 {tema}\n\n{propuesta}\n\nSlide para saber más →",
            "hashtags": f"#{slug_nombre} #{objetivo.replace(' ', '')}",
            "cta": "Swipe up / Link en bio",
            "estructura_json": {
                "formato": "historia",
                "pantallas": [
                    {"numero": 1, "duracion": "15s", "texto": f"💡 {tema}", "sticker": "encuesta"},
                    {"numero": 2, "duracion": "15s", "texto": propuesta[:120], "sticker": "link"},
                ],
            },
        },
        "post": {
            "titulo": f"Post: {tema}",
            "copy": (
                f"✨ {tema}\n\n"
                f"{propuesta}\n\n"
                f"¿Quieres saber cómo {tema.lower()} puede impulsar tu negocio?\n\n"
                f"{servicios}"
            ),
            "hashtags": (
                f"#{slug_nombre} #{slug_tema} #emprendimiento #negociosdigitales #chile #marketing"
            ),
            "cta": f"Escríbenos para conocer más sobre {tema} ✉️",
            "estructura_json": {"formato": "imagen_unica", "caption_lineas": 5},
        },
        "reel": {
            "titulo": f"Reel: {tema}",
            "copy": f"🎬 {tema} en 30 segundos\n\n{propuesta}\n\n¡Compártelo si te fue útil!",
            "hashtags": (
                f"#{slug_nombre} #reels #marketing #{objetivo.replace(' ', '')} #pyme #emprendimiento"
            ),
            "cta": "Síguenos para más contenido 🚀",
            "estructura_json": {
                "formato": "reel",
                "duracion": "30s",
                "escenas": [
                    {"rango": "0-5s", "texto": f"¿Sabes qué es {tema}?"},
                    {"rango": "5-20s", "texto": propuesta[:100]},
                    {"rango": "20-30s", "texto": f"Con {nombre} lo logras — escríbenos"},
                ],
            },
        },
        "campana": {
            "titulo": f"Campaña: {objetivo} con {nombre}",
            "copy": (
                f"🚀 Campaña: {tema}\n\n"
                f"Objetivo: {objetivo}\n\n"
                f"{propuesta}\n\n"
                f"Únete a la campaña →"
            ),
            "hashtags": f"#{slug_nombre} #{slug_tema} #campaña #{objetivo.replace(' ', '')}",
            "cta": "Únete ahora — link en bio 🔗",
            "estructura_json": {
                "formato": "campana",
                "piezas": [
                    {"tipo": "post", "descripcion": "Lanzamiento de campaña"},
                    {"tipo": "historia", "descripcion": "Countdown 3 días antes"},
                    {"tipo": "reel", "descripcion": "Video teaser 15s"},
                    {"tipo": "carrusel", "descripcion": "Beneficios detallados"},
                ],
            },
        },
    }

    return plantillas.get(tipo_contenido, plantillas["post"])
