"""
Agente Estratega — Nexa AI
Genera estrategias mensuales con briefs de contenido orientados a marketing.

# === PUNTO DE CONEXIÓN API ===
# Reemplazar `_generar_simulado` con llamada real a Claude/OpenAI.
# La firma de `generar_estrategia` no debe cambiar.
# === FIN PUNTO DE CONEXIÓN ===
"""

from datetime import date


def generar_estrategia(empresa, memoria_marca) -> dict:
    """
    Genera una estrategia mensual de contenido.
    Retorna: objetivo, pilares_contenido, frecuencia_publicacion,
    publico_objetivo, calendario_json.
    """
    return _generar_simulado(empresa, memoria_marca)


def _generar_simulado(empresa, memoria_marca) -> dict:
    nombre   = empresa.nombre_empresa
    objetivo = empresa.get_objetivo_principal_display()
    tono     = empresa.get_tono_marca_display()
    publico  = empresa.publico_objetivo
    propuesta = (memoria_marca.propuesta_valor if memoria_marca
                 else empresa.descripcion[:200]).strip()

    pilares = _pilares_desde_memoria(empresa, memoria_marca)
    frecuencia = _frecuencia_por_objetivo(empresa.objetivo_principal)
    calendario = _generar_calendario(nombre, empresa.objetivo_principal, pilares, empresa, memoria_marca)

    return {
        "objetivo": (
            f"Este mes {nombre} se enfocará en {objetivo.lower()}, "
            f"comunicando de forma {tono.lower()} hacia {publico[:80].rstrip('.')}. "
            f"{propuesta[:180]}"
        ),
        "pilares_contenido": ", ".join(pilares),
        "frecuencia_publicacion": frecuencia,
        "publico_objetivo": publico,
        "calendario_json": calendario,
    }


# ── Pilares desde memoria de marca ────────────────────────────────────────────

def _pilares_desde_memoria(empresa, memoria_marca) -> list:
    """
    Genera pilares de contenido específicos usando la memoria de marca.
    Prioriza palabras_clave y servicios_principales sobre categorías genéricas.
    """
    if not memoria_marca:
        return _pilares_genericos(empresa.objetivo_principal)

    candidatos = []

    # 1. Palabras clave de marca (mayor prioridad)
    if memoria_marca.palabras_clave:
        kws = [k.strip() for k in memoria_marca.palabras_clave.split(",") if k.strip()]
        candidatos.extend(kws[:3])

    # 2. Servicios principales
    if memoria_marca.servicios_principales and len(candidatos) < 4:
        servicios_raw = memoria_marca.servicios_principales
        for sep in ["\n", ",", ";"]:
            if sep in servicios_raw:
                partes = [s.strip() for s in servicios_raw.split(sep) if s.strip()]
                for p in partes[:3]:
                    # Tomar solo la primera frase si el servicio es largo
                    pilar = p.split(".")[0].split(":")[0].strip()[:40]
                    if len(pilar) > 3:
                        candidatos.append(pilar)
                break

    # Deduplicar y limpiar
    vistos = set()
    resultado = []
    for c in candidatos:
        norm = c.lower().strip()
        if norm not in vistos and len(norm) > 2:
            vistos.add(norm)
            resultado.append(c.capitalize() if c.islower() else c)
        if len(resultado) >= 4:
            break

    # Fallback si la memoria no tenía suficiente información
    if len(resultado) < 3:
        resultado.extend(_pilares_genericos(empresa.objetivo_principal))
        dedup = list(dict.fromkeys(resultado))
        resultado = dedup[:4]

    return resultado[:4]


def _pilares_genericos(objetivo: str) -> list:
    mapa = {
        "ventas":        ["Producto estrella", "Caso de éxito", "Oferta del mes", "Testimonio"],
        "reconocimiento":["Historia de marca", "Valores", "Equipo", "Impacto social"],
        "comunidad":     ["Comunidad", "Detrás de cámaras", "Colaboraciones", "Contenido UGC"],
        "educacion":     ["Tutorial", "Tip práctico", "Mito vs Realidad", "Dato del sector"],
        "confianza":     ["Proceso de trabajo", "Certificación", "FAQ", "Testimonio"],
    }
    return mapa.get(objetivo, ["Educativo", "Inspiracional", "Promocional", "Comunidad"])


# ── Frecuencia ────────────────────────────────────────────────────────────────

def _frecuencia_por_objetivo(objetivo: str) -> str:
    mapa = {
        "ventas":        "5 publicaciones por semana (L-M-X-J-V)",
        "reconocimiento":"4 publicaciones por semana (L-X-V-S)",
        "comunidad":     "6 publicaciones por semana (L-M-X-J-V-S)",
        "educacion":     "3 publicaciones por semana (L-X-V)",
        "confianza":     "3 publicaciones por semana (M-J-S)",
    }
    return mapa.get(objetivo, "3 publicaciones por semana")


# ── Calendario con briefs reales ──────────────────────────────────────────────

def _generar_calendario(nombre, objetivo, pilares, empresa, memoria_marca) -> dict:
    tipos_semana = [
        [("Lunes", "carrusel"), ("Miércoles", "historia"), ("Viernes", "post")],
        [("Martes", "reel"),    ("Jueves", "carrusel"),    ("Sábado", "historia")],
        [("Lunes", "historia"), ("Miércoles", "carrusel"), ("Viernes", "reel")],
        [("Martes", "reel"),    ("Jueves", "historia"),    ("Sábado", "post")],
    ]

    mes_actual = date.today().strftime("%B %Y")
    semanas = []

    for i, semana_config in enumerate(tipos_semana, 1):
        publicaciones = []
        for j, (dia, tipo) in enumerate(semana_config):
            pilar = pilares[j % len(pilares)]
            brief = _brief_contenido(pilar, tipo, empresa, memoria_marca)
            publicaciones.append({
                "dia": dia,
                "tipo": tipo,
                "pilar": pilar,
                "tema": brief["tema"],
                "enfoque": brief["enfoque"],
                "objetivo_pieza": brief["objetivo_pieza"],
                "descripcion": brief["descripcion"],
                "estado": "planificado",
            })
        semanas.append({"semana": i, "publicaciones": publicaciones})

    return {"mes": mes_actual, "empresa": nombre, "semanas": semanas}


# ── Brief de contenido por pilar y tipo ──────────────────────────────────────

def _brief_contenido(pilar: str, tipo: str, empresa, memoria_marca) -> dict:
    """
    Genera un brief de marketing específico para cada combinación pilar + tipo.
    memoria_marca se reserva para personalización avanzada al conectar la API.
    """
    pilar_l = pilar.lower()
    nombre  = empresa.nombre_empresa

    categoria = _categorizar_pilar(pilar_l)
    temas     = _TEMAS_POR_CATEGORIA.get(categoria, _TEMAS_POR_CATEGORIA["general"])
    variante  = temas.get(tipo, temas.get("post"))

    return {
        "tema": variante["tema"].format(nombre=nombre, pilar=pilar),
        "enfoque": variante["enfoque"],
        "objetivo_pieza": variante["objetivo_pieza"],
        "descripcion": f"{variante['tema'].format(nombre=nombre, pilar=pilar)} — {variante['enfoque']}",
    }


def _categorizar_pilar(pilar_l: str) -> str:
    if any(w in pilar_l for w in ["automati", "rpa", "proceso", "flujo"]):
        return "automatizacion"
    if any(w in pilar_l for w in ["ia ", "inteligencia", " ia", "artificial", "machine"]):
        return "ia"
    if any(w in pilar_l for w in ["software", "sistema", "desarrollo", "tecnologi", "digital"]):
        return "software"
    if any(w in pilar_l for w in ["dashboard", "analiti", "dato", "reporte", "bi ", "kpi"]):
        return "datos"
    if any(w in pilar_l for w in ["productiv", "eficienci", "tiempo", "ahorro"]):
        return "productividad"
    if any(w in pilar_l for w in ["transform", "innovaci", "cambio", "futuro"]):
        return "transformacion"
    if any(w in pilar_l for w in ["venta", "lead", "cliente", "comerci"]):
        return "ventas"
    if any(w in pilar_l for w in ["equipo", "team", "persona", "talento", "cultura"]):
        return "equipo"
    if any(w in pilar_l for w in ["caso", "exito", "resultado", "testimoni", "impacto"]):
        return "casos"
    if any(w in pilar_l for w in ["tip", "tutorial", "guia", "aprend", "educat"]):
        return "educacion"
    return "general"


# ── Diccionario de temas por categoría y tipo de contenido ───────────────────

_TEMAS_POR_CATEGORIA = {
    "automatizacion": {
        "carrusel": {
            "tema": "5 tareas que {nombre} puede ayudarte a automatizar esta semana",
            "enfoque": "Mostrar casos concretos donde la automatización ahorra tiempo y reduce errores",
            "objetivo_pieza": "Despertar interés en un diagnóstico de procesos",
        },
        "post": {
            "tema": "¿Cuántas horas pierde tu empresa en tareas manuales?",
            "enfoque": "Conectar el dolor del trabajo repetitivo con la solución que ofrece {nombre}",
            "objetivo_pieza": "Generar identificación y consultas",
        },
        "historia": {
            "tema": "¿Tu empresa automatiza o sigue trabajando manual?",
            "enfoque": "Encuesta para identificar empresas listas para automatizar",
            "objetivo_pieza": "Captar leads calificados a través de la interacción",
        },
        "reel": {
            "tema": "En 30 segundos: qué puede automatizar una empresa hoy",
            "enfoque": "Demostración rápida y visual del impacto de la automatización",
            "objetivo_pieza": "Generar alcance y solicitudes de información",
        },
    },
    "ia": {
        "carrusel": {
            "tema": "Cómo la Inteligencia Artificial puede tomar decisiones por tu empresa",
            "enfoque": "Explicar de forma simple y visual el valor práctico de la IA en negocios",
            "objetivo_pieza": "Educar y generar confianza como referentes en IA",
        },
        "post": {
            "tema": "3 formas en que la IA ya está cambiando empresas como la tuya",
            "enfoque": "Casos reales y accesibles que conecten con el público objetivo",
            "objetivo_pieza": "Posicionar a {nombre} como expertos aplicados en IA",
        },
        "historia": {
            "tema": "¿Ya usas IA en tu empresa?",
            "enfoque": "Encuesta para medir adopción y educar sobre posibilidades",
            "objetivo_pieza": "Segmentar audiencia y generar conversación",
        },
        "reel": {
            "tema": "Lo que la IA puede hacer por tu empresa en menos de un minuto",
            "enfoque": "Demostración visual rápida para desmitificar la IA empresarial",
            "objetivo_pieza": "Viralizar y generar consultas de empresas interesadas",
        },
    },
    "software": {
        "carrusel": {
            "tema": "Por qué tu empresa necesita software hecho a medida (y no solo Excel)",
            "enfoque": "Comparativa visual entre soluciones genéricas y software específico",
            "objetivo_pieza": "Generar interés en un diagnóstico tecnológico",
        },
        "post": {
            "tema": "El software correcto puede duplicar la eficiencia de tu equipo",
            "enfoque": "Demostrar resultados concretos y diferencias frente a herramientas genéricas",
            "objetivo_pieza": "Atraer empresas en etapa de evaluación tecnológica",
        },
        "historia": {
            "tema": "¿Qué herramientas digitales usa tu empresa?",
            "enfoque": "Sondeo para identificar necesidades tecnológicas del público",
            "objetivo_pieza": "Identificar prospectos y generar conversación",
        },
        "reel": {
            "tema": "Antes y después: cómo el software a medida transforma una empresa",
            "enfoque": "Historia visual de transformación real o referencial",
            "objetivo_pieza": "Inspirar y generar solicitudes de propuesta",
        },
    },
    "datos": {
        "carrusel": {
            "tema": "5 decisiones empresariales que no deberías tomar sin datos",
            "enfoque": "Educar sobre la importancia de los datos en decisiones estratégicas",
            "objetivo_pieza": "Posicionar la analítica como necesidad, no lujo",
        },
        "post": {
            "tema": "Tu empresa tiene datos valiosos que probablemente no está aprovechando",
            "enfoque": "Revelar el costo de no analizar la información interna",
            "objetivo_pieza": "Generar urgencia y solicitudes de diagnóstico",
        },
        "historia": {
            "tema": "¿Tu empresa toma decisiones con datos o con intuición?",
            "enfoque": "Encuesta para posicionarse frente a la madurez analítica del mercado",
            "objetivo_pieza": "Captar atención de gerentes y directivos",
        },
        "reel": {
            "tema": "Cómo un dashboard puede cambiar la forma en que diriges tu empresa",
            "enfoque": "Demo visual y rápida del impacto de tener datos en tiempo real",
            "objetivo_pieza": "Generar deseo por herramientas de visualización",
        },
    },
    "productividad": {
        "carrusel": {
            "tema": "Cómo recuperar 10 horas semanales en tu empresa con estas acciones",
            "enfoque": "Tips accionables y concretos para reducir tiempo perdido",
            "objetivo_pieza": "Generar guardados y compartidos",
        },
        "post": {
            "tema": "La productividad no es trabajar más, es trabajar mejor",
            "enfoque": "Cambiar la narrativa sobre eficiencia con ejemplos reales",
            "objetivo_pieza": "Conectar emocionalmente con empresarios que sienten el agotamiento",
        },
        "historia": {
            "tema": "¿Cuánto tiempo pierdes en reuniones innecesarias?",
            "enfoque": "Encuesta con humor para identificar puntos de fricción operacional",
            "objetivo_pieza": "Generar engagement e identificación",
        },
        "reel": {
            "tema": "3 hábitos que las empresas más productivas tienen en común",
            "enfoque": "Contenido rápido, práctico y altamente compartible",
            "objetivo_pieza": "Viralizar y atraer a audiencia empresarial",
        },
    },
    "transformacion": {
        "carrusel": {
            "tema": "Transformación digital: qué es realmente y cómo empezar",
            "enfoque": "Desmitificar el concepto y hacerlo accesible para pymes",
            "objetivo_pieza": "Educar y posicionarse como guía en el proceso",
        },
        "post": {
            "tema": "Las empresas que no se digitalizan hoy, mañana no existen",
            "enfoque": "Crear urgencia sin generar miedo, sino motivación para actuar",
            "objetivo_pieza": "Generar reflexión y consultas",
        },
        "historia": {
            "tema": "¿En qué etapa de transformación digital está tu empresa?",
            "enfoque": "Test rápido de madurez digital para segmentar audiencia",
            "objetivo_pieza": "Identificar empresas en etapa temprana y media",
        },
        "reel": {
            "tema": "Empresas que transformaron su operación con tecnología: resultados reales",
            "enfoque": "Casos de éxito rápidos y concretos de transformación digital",
            "objetivo_pieza": "Inspirar y generar solicitudes",
        },
    },
    "ventas": {
        "carrusel": {
            "tema": "El proceso de ventas que usan las empresas que más crecen",
            "enfoque": "Mostrar un framework de ventas moderno y accionable",
            "objetivo_pieza": "Generar guardados y consultas sobre metodología",
        },
        "post": {
            "tema": "¿Por qué tus prospectos no convierten? La respuesta te va a sorprender",
            "enfoque": "Identificar el problema real detrás de las ventas perdidas",
            "objetivo_pieza": "Generar identificación y solicitudes de consultoría",
        },
        "historia": {
            "tema": "¿Cuánto tiempo demora tu ciclo de ventas?",
            "enfoque": "Benchmark rápido para que el prospecto se autoevalúe",
            "objetivo_pieza": "Captar prospectos con proceso de ventas largo",
        },
        "reel": {
            "tema": "El error de ventas que más le cuesta a las pymes",
            "enfoque": "Hook polémico con solución concreta al final",
            "objetivo_pieza": "Viralizar y atraer prospectos con dolor claro",
        },
    },
    "equipo": {
        "carrusel": {
            "tema": "Las personas detrás de {nombre}: por qué el equipo lo es todo",
            "enfoque": "Humanizar la marca y mostrar el valor del talento interno",
            "objetivo_pieza": "Generar confianza y conexión emocional con la marca",
        },
        "post": {
            "tema": "Construir un gran equipo es la mejor inversión que puede hacer una empresa",
            "enfoque": "Reflexión sobre cultura organizacional con ejemplos concretos",
            "objetivo_pieza": "Posicionar valores de la empresa y atraer talento",
        },
        "historia": {
            "tema": "¿Qué valoras más en tu equipo de trabajo?",
            "enfoque": "Encuesta para humanizar la marca y generar conversación",
            "objetivo_pieza": "Aumentar engagement y fortalecer comunidad",
        },
        "reel": {
            "tema": "Un día en {nombre}: cómo trabajamos para transformar empresas",
            "enfoque": "Detrás de cámaras auténtico que muestre la cultura interna",
            "objetivo_pieza": "Humanizar la marca y atraer clientes y talento",
        },
    },
    "casos": {
        "carrusel": {
            "tema": "Cómo ayudamos a [cliente] a transformar su operación con tecnología",
            "enfoque": "Storytelling de caso real: problema → solución → resultado medible",
            "objetivo_pieza": "Generar prueba social y solicitudes similares",
        },
        "post": {
            "tema": "Resultados reales: lo que logramos con uno de nuestros clientes este trimestre",
            "enfoque": "Compartir métricas y logros concretos de forma accesible",
            "objetivo_pieza": "Construir credibilidad y atraer nuevos prospectos",
        },
        "historia": {
            "tema": "¿Te gustaría lograr resultados como este?",
            "enfoque": "Teaser de caso de éxito con llamada a la acción clara",
            "objetivo_pieza": "Derivar tráfico al perfil o sitio web",
        },
        "reel": {
            "tema": "De este problema a este resultado: el caso de uno de nuestros clientes",
            "enfoque": "Narrativa visual rápida de transformación con datos reales",
            "objetivo_pieza": "Viralizar y generar solicitudes por identificación",
        },
    },
    "educacion": {
        "carrusel": {
            "tema": "Guía completa de {pilar}: todo lo que necesitas saber en 5 slides",
            "enfoque": "Contenido educativo denso pero visual, diseñado para ser guardado",
            "objetivo_pieza": "Posicionarse como referente y generar guardados",
        },
        "post": {
            "tema": "3 conceptos sobre {pilar} que todo empresario debería conocer",
            "enfoque": "Simplificar conceptos técnicos con lenguaje accesible y ejemplos",
            "objetivo_pieza": "Educar y generar confianza como expertos",
        },
        "historia": {
            "tema": "¿Cuánto sabes sobre {pilar}?",
            "enfoque": "Quiz o encuesta de conocimiento para educar de forma entretenida",
            "objetivo_pieza": "Generar engagement e identificar nivel de madurez",
        },
        "reel": {
            "tema": "{pilar} explicado en 30 segundos — sin tecnicismos",
            "enfoque": "Simplificación máxima con gancho fuerte al inicio",
            "objetivo_pieza": "Viralizar y atraer audiencia nueva",
        },
    },
    "general": {
        "carrusel": {
            "tema": "5 razones para trabajar con {nombre}",
            "enfoque": "Mostrar propuesta de valor de forma visual y accesible",
            "objetivo_pieza": "Generar consideración e interés en los servicios",
        },
        "post": {
            "tema": "Por qué {nombre} es diferente al resto del mercado",
            "enfoque": "Articular la diferenciación de la marca con ejemplos reales",
            "objetivo_pieza": "Posicionar y generar consultas",
        },
        "historia": {
            "tema": "¿Conoces lo que hace {nombre}?",
            "enfoque": "Introducción rápida a los servicios con interacción",
            "objetivo_pieza": "Aumentar awareness de la marca",
        },
        "reel": {
            "tema": "Lo que hacemos en {nombre} puede cambiar tu empresa",
            "enfoque": "Pitch visual rápido con prueba de valor",
            "objetivo_pieza": "Generar visitas al perfil y consultas",
        },
    },
}
