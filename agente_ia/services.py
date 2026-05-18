import re
import unicodedata

from difflib import SequenceMatcher

from django.db.models import F

from .models import (
    RespuestaConocimiento,
    PreguntaAprendida,
)


def normalizar_texto(texto):

    if not texto:
        return ""

    texto = texto.lower().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = re.sub(
        r"[^a-z0-9ñ\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def separar_palabras_clave(texto):

    if not texto:
        return []

    resultado = []

    for palabra in texto.split(","):

        palabra = normalizar_texto(palabra)

        if palabra:
            resultado.append(palabra)

    return resultado


def similitud_texto(a, b):

    return SequenceMatcher(
        None,
        normalizar_texto(a),
        normalizar_texto(b),
    ).ratio()


def buscar_en_conocimiento(mensaje_usuario):

    respuestas = (
        RespuestaConocimiento.objects
        .filter(activa=True)
        .select_related("categoria")
    )

    mejor_respuesta = None
    mejor_puntaje = 0

    mensaje_normalizado = normalizar_texto(
        mensaje_usuario
    )

    palabras_usuario = set(
        mensaje_normalizado.split()
    )

    for respuesta in respuestas:

        puntaje = 0

        palabras_clave = separar_palabras_clave(
            respuesta.palabras_clave
        )

        for palabra_clave in palabras_clave:

            if palabra_clave in mensaje_normalizado:
                puntaje += 12

            palabras_clave_set = set(
                palabra_clave.split()
            )

            coincidencias = palabras_usuario.intersection(
                palabras_clave_set
            )

            puntaje += len(coincidencias) * 4

            similitud = similitud_texto(
                mensaje_normalizado,
                palabra_clave
            )

            if similitud >= 0.72:
                puntaje += int(similitud * 10)

        puntaje += respuesta.prioridad * 2

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_respuesta = respuesta

    if mejor_respuesta and mejor_puntaje >= 22:

        RespuestaConocimiento.objects.filter(
            id=mejor_respuesta.id
        ).update(
            veces_utilizada=F("veces_utilizada") + 1
        )

        return mejor_respuesta.respuesta

    return None


def buscar_en_preguntas_aprendidas(mensaje_usuario):

    preguntas = (
        PreguntaAprendida.objects
        .filter(
            respondida=True
        )
    )

    mejor = None

    mejor_similitud = 0

    for pregunta in preguntas:

        similitud = similitud_texto(
            mensaje_usuario,
            pregunta.pregunta
        )

        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor = pregunta

    if mejor and mejor_similitud >= 0.78:
        return mejor.respuesta_sugerida

    return None


def registrar_pregunta_no_resuelta(mensaje_usuario):

    preguntas_existentes = (
        PreguntaAprendida.objects
        .filter(
            respondida=False
        )
    )

    for pregunta in preguntas_existentes:

        similitud = similitud_texto(
            mensaje_usuario,
            pregunta.pregunta
        )

        if similitud >= 0.82:

            pregunta.veces_preguntada += 1

            pregunta.save(
                update_fields=[
                    "veces_preguntada",
                    "ultima_vez",
                ]
            )

            return pregunta

    return PreguntaAprendida.objects.create(
        pregunta=mensaje_usuario,
        respondida=False,
    )


def generar_respuesta_fallback():

    return """
Gracias por contarme tu necesidad.

Aún no tengo una respuesta específica cargada para ese caso,
pero IDS Digital puede ayudarte a evaluar una solución tecnológica.

Dependiendo del problema, podría tratarse de:

• automatización de procesos
• desarrollo de software
• dashboards
• CRM
• integración de plataformas
• inteligencia artificial
• sistemas internos
• reportería y control operacional

Te recomiendo dejar tus datos para que el equipo de IDS Digital
pueda revisar tu caso y entregarte una orientación más precisa.
""".strip()


def generar_diagnostico_ia(mensajes):

    if not mensajes:

        return (
            "Hola. Soy el agente digital de IDS Digital. "
            "Cuéntame qué proceso deseas mejorar, automatizar o transformar."
        )

    ultimo_mensaje = ""

    for mensaje in reversed(mensajes):

        if mensaje.get("role") == "user":

            ultimo_mensaje = (
                mensaje.get("content", "").strip()
            )

            break

    if not ultimo_mensaje:

        return (
            "Cuéntame un poco más sobre tu necesidad."
        )

    respuesta_conocimiento = buscar_en_conocimiento(
        ultimo_mensaje
    )

    if respuesta_conocimiento:
        return respuesta_conocimiento

    respuesta_aprendida = buscar_en_preguntas_aprendidas(
        ultimo_mensaje
    )

    if respuesta_aprendida:
        return respuesta_aprendida

    registrar_pregunta_no_resuelta(
        ultimo_mensaje
    )

    return generar_respuesta_fallback()