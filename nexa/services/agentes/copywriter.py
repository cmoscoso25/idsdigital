"""
Agente Copywriter — Nexa AI
Genera contenido completo para cada pieza del calendario mensual.

# === PUNTO DE CONEXIÓN API ===
# Reemplazar `_generar_simulado` con llamada a Claude/OpenAI API.
# Mantener la misma firma de retorno: titulo, copy, hashtags, cta, estructura_json.
# === FIN PUNTO DE CONEXIÓN ===
"""


def generar_contenido_completo(
    empresa,
    memoria_marca,
    tipo_contenido: str,
    pilar: str,
    objetivo: str,
    semana: int = 1,
) -> dict:
    """
    Genera una pieza de contenido completa para el calendario mensual.
    Retorna dict con: titulo, copy, hashtags, cta, estructura_json.
    """
    return _generar_simulado(empresa, memoria_marca, tipo_contenido, pilar, objetivo, semana)


def generar_copy(empresa, memoria_marca, tipo_contenido: str, tema: str, objetivo: str) -> dict:
    """Compatibilidad con llamadas existentes desde generar_contenido.py."""
    resultado = generar_contenido_completo(
        empresa, memoria_marca, tipo_contenido, pilar=tema, objetivo=objetivo
    )
    return {
        "copy": resultado["copy"],
        "cta": resultado["cta"],
        "hashtags": resultado["hashtags"],
    }


def _generar_simulado(empresa, memoria_marca, tipo_contenido, pilar, objetivo, semana) -> dict:
    nombre = empresa.nombre_empresa
    tono = empresa.tono_marca
    propuesta = memoria_marca.propuesta_valor if memoria_marca else empresa.descripcion[:150]
    servicios = memoria_marca.servicios_principales[:120] if memoria_marca else empresa.rubro
    slug_nombre = nombre.replace(" ", "")
    slug_pilar = pilar.replace(" ", "")

    apertura = _apertura(tono, nombre)
    titulo = _titulo(tipo_contenido, pilar, nombre, semana)
    copy = _copy(apertura, propuesta, pilar, objetivo, tono, nombre)
    hashtags = _hashtags(slug_nombre, slug_pilar, objetivo, tono)
    cta = _cta(tono, nombre, pilar)
    estructura = _estructura(tipo_contenido, pilar, propuesta, servicios, nombre, semana)

    return {
        "titulo": titulo,
        "copy": copy,
        "hashtags": hashtags,
        "cta": cta,
        "estructura_json": estructura,
    }


def _apertura(tono: str, nombre: str) -> str:
    aperturas = {
        "profesional": f"En {nombre} sabemos que",
        "cercano": f"¡Hola! En {nombre} creemos que",
        "inspirador": f"✨ Cada día es una oportunidad. En {nombre},",
        "humoristico": f"😄 Seamos honestos:",
        "exclusivo": f"Solo para quienes buscan lo mejor:",
        "educativo": f"¿Sabías que",
    }
    return aperturas.get(tono, f"En {nombre},")


def _titulo(tipo: str, pilar: str, nombre: str, semana: int) -> str:
    prefijos = {
        "carrusel": f"📌 {pilar} — Guía de {nombre}",
        "historia": f"💡 {pilar} al instante",
        "post": f"✨ {pilar}: lo que necesitas saber",
        "reel": f"🎬 {pilar} en 30 segundos",
        "campana": f"🚀 Campaña: {pilar}",
    }
    return prefijos.get(tipo, f"{pilar} — {nombre}") + f" (Sem. {semana})"


def _copy(apertura: str, propuesta: str, pilar: str, objetivo: str, tono: str, nombre: str) -> str:
    emojis = {"cercano": "👇", "inspirador": "🌟", "educativo": "💡", "profesional": "→"}
    emoji = emojis.get(tono, "→")
    return (
        f"{apertura} {propuesta[:100]}\n\n"
        f"Hoy hablamos sobre: {pilar}\n\n"
        f"Nuestro objetivo: {objetivo}\n\n"
        f"¿Quieres saber cómo {pilar.lower()} puede transformar tu negocio? {emoji}"
    )


def _hashtags(slug_nombre: str, slug_pilar: str, objetivo: str, tono: str) -> str:
    base = f"#{slug_nombre} #{slug_pilar} #marketing #pyme #emprendimiento"
    extras = {
        "educativo": " #aprendizaje #tips",
        "inspirador": " #inspiracion #motivacion",
        "cercano": " #comunidad #juntos",
        "profesional": " #negocios #estrategia",
    }
    return base + extras.get(tono, "")


def _cta(tono: str, nombre: str, pilar: str) -> str:
    ctas = {
        "profesional": f"Contáctanos para saber cómo {pilar} puede impactar tu empresa →",
        "cercano": f"Escríbenos, estamos para ayudarte con {pilar} 💬",
        "inspirador": f"Da el primer paso hoy. {nombre} está contigo 🚀",
        "humoristico": f"No te quedes fuera, escríbenos ya 😄",
        "exclusivo": f"Solicita tu consulta exclusiva →",
        "educativo": f"¿Tienes dudas sobre {pilar}? Pregúntanos 💡",
    }
    return ctas.get(tono, f"Escríbenos y hablemos de {pilar}")


def _estructura(tipo: str, pilar: str, propuesta: str, servicios: str, nombre: str, semana: int) -> dict:
    estructuras = {
        "carrusel": {
            "formato": "carrusel",
            "diapositivas": [
                {"numero": 1, "tipo": "portada", "texto": f"📌 {pilar}"},
                {"numero": 2, "tipo": "contenido", "texto": propuesta[:100]},
                {"numero": 3, "tipo": "contenido", "texto": f"En {nombre}: {servicios[:80]}"},
                {"numero": 4, "tipo": "cierre", "texto": f"¿Por qué {pilar}?"},
                {"numero": 5, "tipo": "cta", "texto": "Contáctanos hoy →"},
            ],
        },
        "historia": {
            "formato": "historia",
            "pantallas": [
                {"numero": 1, "duracion": "7s", "texto": f"💡 {pilar}", "sticker": "encuesta"},
                {"numero": 2, "duracion": "7s", "texto": propuesta[:100], "sticker": "link"},
                {"numero": 3, "duracion": "6s", "texto": "Más info en el link 👇", "sticker": None},
            ],
        },
        "reel": {
            "formato": "reel",
            "duracion": "30s",
            "escenas": [
                {"rango": "0-7s", "texto": f"🎬 {pilar} — ¿lo conoces?"},
                {"rango": "7-20s", "texto": propuesta[:80]},
                {"rango": "20-30s", "texto": f"Con {nombre} lo logramos"},
            ],
        },
        "post": {
            "formato": "imagen_unica",
            "caption_lineas": 5,
            "pilar": pilar,
        },
        "campana": {
            "formato": "campana",
            "piezas": [
                {"tipo": "post", "descripcion": f"Lanzamiento — {pilar}"},
                {"tipo": "historia", "descripcion": "Countdown"},
                {"tipo": "reel", "descripcion": "Teaser 15s"},
                {"tipo": "carrusel", "descripcion": "Beneficios"},
            ],
        },
    }
    return estructuras.get(tipo, {"formato": tipo, "pilar": pilar, "semana": semana})
