"""
Director Creativo — Nexa AI
Selecciona el estilo visual óptimo para cada pieza Instagram.
Garantiza variedad: nunca repite el mismo estilo consecutivo para la misma empresa.
"""

# ── Catálogo completo de estilos por formato ──────────────────────────────────

ESTILOS_INSTAGRAM = {
    "post": [
        {
            "id": "corporate_kpi",
            "nombre": "Corporate KPI",
            "descripcion": "Métricas y datos como protagonistas. Impacto numérico inmediato.",
            "afinidad_objetivo": ["venta", "resultado", "eficienci", "roi", "crecimient"],
            "afinidad_tema": ["resultado", "dato", "kpi", "número", "porcentaje", "eficienci"],
        },
        {
            "id": "minimalista_premium",
            "nombre": "Minimalista Premium",
            "descripcion": "Tipografía masiva, espacio, mensaje directo. Sin ruido.",
            "afinidad_objetivo": ["reconocimient", "marca", "posicion", "premium"],
            "afinidad_tema": ["transform", "vision", "liderazg", "innovaci", "futuro"],
        },
        {
            "id": "problema_solucion",
            "nombre": "Problema / Solución",
            "descripcion": "División visual: el dolor arriba, la respuesta abajo.",
            "afinidad_objetivo": ["venta", "conver", "lead"],
            "afinidad_tema": ["problema", "error", "dificult", "reto", "desafio"],
        },
        {
            "id": "estadistica",
            "nombre": "Estadística",
            "descripcion": "Un número impactante llena el frame. Sin ruido visual.",
            "afinidad_objetivo": ["educa", "reconocimient"],
            "afinidad_tema": ["dato", "estadist", "porcentaj", "estudio", "investigaci"],
        },
        {
            "id": "testimonio",
            "nombre": "Testimonio",
            "descripcion": "Cita de cliente con identidad de marca. Prueba social.",
            "afinidad_objetivo": ["confianz", "comunidad"],
            "afinidad_tema": ["cliente", "testimon", "resultado", "caso", "experienci"],
        },
    ],
    "historia": [
        {
            "id": "encuesta",
            "nombre": "Encuesta",
            "descripcion": "Pregunta + opciones interactivas. Máximo engagement.",
            "afinidad_objetivo": ["comunidad", "engagement"],
            "afinidad_tema": ["pregunta", "opini", "¿qué", "cual"],
        },
        {
            "id": "quiz",
            "nombre": "Quiz",
            "descripcion": "Trivia de la marca. Divertido, educativo y viral.",
            "afinidad_objetivo": ["educa", "comunidad"],
            "afinidad_tema": ["sabias", "verdad", "mito", "trivia"],
        },
        {
            "id": "antes_despues",
            "nombre": "Antes / Después",
            "descripcion": "Transformación visual: pantalla 1 problema, pantalla 3 solución.",
            "afinidad_objetivo": ["venta", "conver"],
            "afinidad_tema": ["antes", "después", "transform", "cambio", "mejora"],
        },
        {
            "id": "cta_urgente",
            "nombre": "CTA Urgente",
            "descripcion": "3 pantallas que construyen urgencia hacia una acción.",
            "afinidad_objetivo": ["venta", "lead", "conver"],
            "afinidad_tema": ["oferta", "limit", "hoy", "ahora", "lanzamient"],
        },
        {
            "id": "detras_camaras",
            "nombre": "Detrás de Cámaras",
            "descripcion": "Look informal y auténtico. Proceso interno visible.",
            "afinidad_objetivo": ["comunidad", "confianz"],
            "afinidad_tema": ["proceso", "equipo", "trabaj", "como lo hacemos"],
        },
    ],
    "carrusel": [
        {
            "id": "problema_solucion",
            "nombre": "Problema → Solución",
            "descripcion": "Narrativa clásica de 6 slides: portada→problema→consecuencia→solución→beneficio→CTA.",
            "afinidad_objetivo": ["venta", "lead"],
            "afinidad_tema": ["problema", "soluci"],
        },
        {
            "id": "lista_numerada",
            "nombre": "Lista (Top N)",
            "descripcion": "Los mejores tips/razones numerados. Slides con 01, 02, 03...",
            "afinidad_objetivo": ["educa", "comunidad"],
            "afinidad_tema": ["top", "list", "razones", "tips", "consejos", "claves"],
        },
        {
            "id": "caso_exito",
            "nombre": "Caso de Éxito",
            "descripcion": "Historia de cliente: desafío, proceso y resultado.",
            "afinidad_objetivo": ["confianz", "venta"],
            "afinidad_tema": ["caso", "exito", "cliente", "resultado"],
        },
        {
            "id": "tutorial_pasos",
            "nombre": "Tutorial Paso a Paso",
            "descripcion": "Cómo hacer X. Slides con PASO 01, 02, 03...",
            "afinidad_objetivo": ["educa"],
            "afinidad_tema": ["como", "tutorial", "paso", "guia", "aprende", "hacer"],
        },
        {
            "id": "mitos_realidad",
            "nombre": "Mitos vs Realidad",
            "descripcion": "Desmiente creencias erróneas. Slides alternando ❌ mito y ✓ realidad.",
            "afinidad_objetivo": ["educa", "confianz"],
            "afinidad_tema": ["mito", "realidad", "verdad", "mentira"],
        },
    ],
    "reel": [
        {
            "id": "hook_solucion",
            "nombre": "Hook + Solución",
            "descripcion": "Gancho, problema, solución, beneficio, CTA.",
            "afinidad_objetivo": ["venta", "lead"],
            "afinidad_tema": ["como", "por qué", "soluci"],
        },
        {
            "id": "caso_exito",
            "nombre": "Caso de Éxito",
            "descripcion": "Historia real de cliente con resultado comprobable.",
            "afinidad_objetivo": ["confianz", "venta"],
            "afinidad_tema": ["caso", "exito", "cliente", "resultado"],
        },
        {
            "id": "tutorial_rapido",
            "nombre": "Tutorial Rápido",
            "descripcion": "3-5 pasos concretos en 30 segundos.",
            "afinidad_objetivo": ["educa"],
            "afinidad_tema": ["como", "tutorial", "paso", "aprende"],
        },
        {
            "id": "error_comun",
            "nombre": "Error Común",
            "descripcion": "El error que cometes + la forma correcta de hacerlo.",
            "afinidad_objetivo": ["educa", "confianz"],
            "afinidad_tema": ["error", "equivoca", "mal", "incorrecto", "evita"],
        },
        {
            "id": "tendencia_educativa",
            "nombre": "Tendencia Educativa",
            "descripcion": "Explica una tendencia del sector de forma clara.",
            "afinidad_objetivo": ["educa", "reconocimient"],
            "afinidad_tema": ["tendencia", "futuro", "nuevo", "innovaci"],
        },
    ],
}


# ── Selección inteligente ─────────────────────────────────────────────────────

def seleccionar_estilo(tipo: str, empresa, contenido) -> dict:
    """
    Selecciona el estilo visual óptimo garantizando rotación completa.
    - Excluye los últimos (N-1) estilos usados → fuerza ciclo por todos los N estilos.
    - Prioriza afinidad con el objetivo/tema del contenido.
    - Cuando scores son iguales, usa rotación determinística para garantizar variedad.
    Retorna el dict del estilo con campo adicional 'motivo_seleccion'.
    """
    from nexa.models import CreatividadInstagram

    estilos = ESTILOS_INSTAGRAM.get(tipo, ESTILOS_INSTAGRAM["post"])
    n = len(estilos)

    # Rastrear los últimos (n-1) estilos usados para forzar el ciclo completo
    recientes_ids = list(
        CreatividadInstagram.objects
        .filter(contenido__empresa=empresa, tipo=tipo)
        .exclude(estilo="")
        .order_by("-fecha_actualizacion", "-pk")
        .values_list("estilo", flat=True)[: n - 1]
    )

    candidatos = [e for e in estilos if e["id"] not in recientes_ids]
    if not candidatos:
        # Todos usados recientemente — excluir solo el más reciente
        candidatos = [e for e in estilos if e["id"] != recientes_ids[0]] if recientes_ids else list(estilos)
    if not candidatos:
        candidatos = list(estilos)

    # Total de creatividades existentes → offset para rotación determinística
    total_existentes = CreatividadInstagram.objects.filter(
        contenido__empresa=empresa, tipo=tipo
    ).count()

    # Texto de referencia para scoring
    texto_ref = " ".join(filter(None, [
        contenido.titulo,
        (contenido.copy[:200] if hasattr(contenido, "copy") else ""),
        (contenido.cta or ""),
        (getattr(empresa, "objetivo_principal", "") or ""),
        (getattr(empresa, "rubro", "") or ""),
    ])).lower()

    # Scoring: afinidad objetivo (+2) + afinidad tema (+1)
    scored = []
    for i, e in enumerate(candidatos):
        score = 0
        for af in e.get("afinidad_objetivo", []):
            if af in texto_ref:
                score += 2
        for af in e.get("afinidad_tema", []):
            if af in texto_ref:
                score += 1
        scored.append((score, i, e))

    max_score = max(s[0] for s in scored)

    if max_score == 0:
        # Sin afinidad: rotación determinística por total de existentes
        idx = total_existentes % len(candidatos)
        selected = candidatos[idx]
    else:
        # Con afinidad: el de mayor score; empate → rotación determinística
        top = [s for s in scored if s[0] == max_score]
        idx = total_existentes % len(top)
        selected = top[idx][2]

    ultimo = recientes_ids[0] if recientes_ids else None
    motivo = _construir_motivo(selected, ultimo, texto_ref)
    return {**selected, "motivo_seleccion": motivo}


def _construir_motivo(estilo: dict, ultimo: str | None, texto_ref: str) -> str:
    nombre = estilo["nombre"]
    if ultimo:
        nombre_anterior = _nombre_por_id(ultimo)
        return (
            f"'{nombre}' seleccionado para variar respecto a '{nombre_anterior}' "
            f"y garantizar diversidad visual en la biblioteca."
        )
    afines = [af for af in estilo.get("afinidad_tema", []) if af in texto_ref]
    if afines:
        return f"'{nombre}' elegido por afinidad temática con el contenido: {', '.join(afines[:2])}."
    return f"'{nombre}' seleccionado como estilo óptimo para este tipo de contenido."


def _nombre_por_id(estilo_id: str) -> str:
    for estilos in ESTILOS_INSTAGRAM.values():
        for e in estilos:
            if e["id"] == estilo_id:
                return e["nombre"]
    return estilo_id


def get_estilo_nombre(tipo: str, estilo_id: str) -> str:
    """Retorna el nombre legible de un estilo dado su ID y tipo."""
    for e in ESTILOS_INSTAGRAM.get(tipo, []):
        if e["id"] == estilo_id:
            return e["nombre"]
    return estilo_id
