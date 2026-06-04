"""
Servicio de generación de contenido para Nexa AI.
Delega al Agente Copywriter para mantener una única fuente de verdad.

PUNTO DE CONEXIÓN API: cuando se active Claude/OpenAI, editar solo
nexa/services/agentes/copywriter.py — este módulo no requiere cambios.
"""

from .agentes.copywriter import generar_contenido_completo


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
    """
    return generar_contenido_completo(
        empresa=empresa,
        memoria_marca=memoria_marca,
        tipo_contenido=tipo_contenido,
        pilar=tema,
        objetivo=objetivo,
    )
