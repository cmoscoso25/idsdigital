"""
Agente Copywriter — Nexa AI
Especializado en generar copy persuasivo adaptado al tono de marca.

# === PUNTO DE CONEXIÓN API ===
# Reemplazar `generar_copy` con llamada a Claude/OpenAI API.
# === FIN PUNTO DE CONEXIÓN ===
"""


def generar_copy(empresa, memoria_marca, tipo_contenido: str, tema: str, objetivo: str) -> dict:
    """
    Genera copy para un tipo específico de contenido.
    Retorna dict con: copy, cta, hashtags.
    """
    return _generar_simulado(empresa, memoria_marca, tipo_contenido, tema, objetivo)


def _generar_simulado(empresa, memoria_marca, tipo_contenido, tema, objetivo) -> dict:
    nombre = empresa.nombre_empresa
    tono = empresa.get_tono_marca_display()
    propuesta = memoria_marca.propuesta_valor if memoria_marca else empresa.descripcion[:150]

    aperturas = {
        "profesional": f"En {nombre} sabemos que",
        "cercano": f"¡Hola! En {nombre} creemos que",
        "inspirador": f"✨ Cada día es una oportunidad. En {nombre},",
        "humoristico": f"😄 Seamos honestos:",
        "exclusivo": f"Solo para quienes buscan lo mejor:",
        "educativo": f"¿Sabías que",
    }
    apertura = aperturas.get(empresa.tono_marca, f"En {nombre},")

    return {
        "copy": f"{apertura} {propuesta[:120]}\n\n{tema}\n\nObjetivo: {objetivo}",
        "cta": f"Escríbenos hoy y descubre cómo {nombre} puede ayudarte 👇",
        "hashtags": f"#{nombre.replace(' ', '')} #{tema.replace(' ', '')} #marketing #pyme",
    }
