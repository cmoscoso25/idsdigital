"""
Agente Estratega — Nexa AI
Genera estrategias mensuales de contenido basadas en la memoria de marca.

# === PUNTO DE CONEXIÓN API ===
# Reemplazar `_generar_simulado` con llamada real a Claude/OpenAI cuando
# se active la integración. La firma de `generar_estrategia` no debe cambiar.
# === FIN PUNTO DE CONEXIÓN ===
"""

from datetime import date


def generar_estrategia(empresa, memoria_marca) -> dict:
    """
    Genera una estrategia mensual de contenido.
    Retorna dict con: objetivo, pilares_contenido, frecuencia_publicacion,
    publico_objetivo, calendario_json.
    """
    return _generar_simulado(empresa, memoria_marca)


def _generar_simulado(empresa, memoria_marca) -> dict:
    nombre = empresa.nombre_empresa
    objetivo = empresa.get_objetivo_principal_display()
    tono = empresa.get_tono_marca_display()
    publico = empresa.publico_objetivo
    propuesta = memoria_marca.propuesta_valor if memoria_marca else empresa.descripcion[:200]
    servicios = memoria_marca.servicios_principales[:200] if memoria_marca else ""

    pilares = _pilares_por_objetivo(empresa.objetivo_principal, nombre, servicios)
    frecuencia = _frecuencia_por_objetivo(empresa.objetivo_principal)
    calendario = _generar_calendario(nombre, empresa.objetivo_principal, pilares, tono)

    return {
        "objetivo": f"Durante este mes, {nombre} se enfocará en {objetivo.lower()} a través de contenido {tono.lower()} que conecte con {publico[:100]}. Propuesta de valor: {propuesta[:200]}",
        "pilares_contenido": ", ".join(pilares),
        "frecuencia_publicacion": frecuencia,
        "publico_objetivo": publico,
        "calendario_json": calendario,
    }


def _pilares_por_objetivo(objetivo, nombre, servicios) -> list:
    base = {
        "ventas": ["Producto/Servicio", "Casos de éxito", "Oferta especial", "Testimonio"],
        "reconocimiento": ["Historia de marca", "Valores", "Equipo", "Impacto"],
        "comunidad": ["Preguntas a la comunidad", "Detrás de cámaras", "Colaboraciones", "User content"],
        "educacion": ["Tutorial", "Tip del día", "Mito vs Realidad", "Datos del sector"],
        "confianza": ["Proceso de trabajo", "Certificaciones", "Preguntas frecuentes", "Testimonio"],
    }
    return base.get(objetivo, ["Educativo", "Inspiracional", "Promocional", "Comunidad"])


def _frecuencia_por_objetivo(objetivo) -> str:
    mapa = {
        "ventas": "5 publicaciones por semana (L-M-X-J-V)",
        "reconocimiento": "4 publicaciones por semana (L-X-V-S)",
        "comunidad": "6 publicaciones por semana (L-M-X-J-V-S)",
        "educacion": "3 publicaciones por semana (L-X-V)",
        "confianza": "3 publicaciones por semana (M-J-S)",
    }
    return mapa.get(objetivo, "3 publicaciones por semana")


def _generar_calendario(nombre, objetivo, pilares, tono) -> dict:
    tipos_semana = [
        [("Lunes", "carrusel"), ("Miércoles", "historia"), ("Viernes", "post")],
        [("Martes", "reel"), ("Jueves", "carrusel"), ("Sábado", "historia")],
        [("Lunes", "historia"), ("Miércoles", "carrusel"), ("Viernes", "reel")],
        [("Martes", "reel"), ("Jueves", "historia"), ("Sábado", "post")],
    ]

    mes_actual = date.today().strftime("%B %Y")
    semanas = []

    for i, semana_config in enumerate(tipos_semana, 1):
        publicaciones = []
        for j, (dia, tipo) in enumerate(semana_config):
            pilar = pilares[j % len(pilares)]
            publicaciones.append({
                "dia": dia,
                "tipo": tipo,
                "pilar": pilar,
                "descripcion": f"{tipo.capitalize()} sobre: {pilar} — tono {tono.lower()}",
                "estado": "planificado",
            })
        semanas.append({"semana": i, "publicaciones": publicaciones})

    return {"mes": mes_actual, "empresa": nombre, "semanas": semanas}
