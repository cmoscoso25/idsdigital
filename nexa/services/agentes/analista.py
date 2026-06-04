"""
Agente Analista — Nexa AI
Analiza rendimiento de contenidos y genera recomendaciones.

# === PUNTO DE CONEXIÓN API ===
# Cuando se active Meta Graph API, reemplazar `analizar_rendimiento`
# con lectura real de métricas de Instagram/Facebook.
# === FIN PUNTO DE CONEXIÓN ===
"""


def analizar_rendimiento(empresa, contenidos_qs) -> dict:
    """
    Analiza los contenidos generados y produce recomendaciones.
    Retorna dict con: resumen, recomendaciones, proximos_pasos.
    """
    return _analizar_simulado(empresa, contenidos_qs)


def _analizar_simulado(empresa, contenidos_qs) -> dict:
    total = contenidos_qs.count()
    por_tipo = {}
    por_estado = {}

    for c in contenidos_qs:
        por_tipo[c.tipo_contenido] = por_tipo.get(c.tipo_contenido, 0) + 1
        por_estado[c.estado] = por_estado.get(c.estado, 0) + 1

    tipo_top = max(por_tipo, key=por_tipo.get) if por_tipo else "post"
    borradores = por_estado.get("borrador", 0)

    return {
        "resumen": {
            "total_contenidos": total,
            "por_tipo": por_tipo,
            "por_estado": por_estado,
        },
        "recomendaciones": [
            f"El formato '{tipo_top}' es tu más usado — considera diversificar.",
            f"Tienes {borradores} borrador(es) pendientes de aprobación.",
            f"Publica al menos 3 veces por semana para mantener engagement.",
            "Alterna entre carruseles educativos y posts de comunidad.",
        ],
        "proximos_pasos": [
            "Aprobar contenidos en borrador",
            "Planificar publicación de la próxima semana",
            "Revisar y actualizar memoria de marca si cambió el enfoque",
        ],
    }
