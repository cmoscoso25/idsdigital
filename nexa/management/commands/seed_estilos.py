from django.core.management.base import BaseCommand
from nexa.models import EstiloVisualInstagram

ESTILOS = [
    # ── POST (10 estilos) ──────────────────────────────────────────────────
    {
        "codigo": "corporate_kpi",
        "nombre": "Corporate KPI",
        "descripcion": "Gradiente de marca, SVG chip de categoría, fila de 3 KPIs y CTA premium.",
        "categoria": "corporativo",
    },
    {
        "codigo": "minimalista_premium",
        "nombre": "Minimalista Premium",
        "descripcion": "Fondo negro, borde izquierdo de color, tipografía enorme sin KPI.",
        "categoria": "editorial",
    },
    {
        "codigo": "problema_solucion",
        "nombre": "Problema / Solución",
        "descripcion": "Split 38/62 izquierda oscura + derecha gradiente, columna problema/solución.",
        "categoria": "narrativo",
    },
    {
        "codigo": "estadistica",
        "nombre": "Estadística Hero",
        "descripcion": "Número gigante con glow, 3 barras de progreso con métricas por categoría.",
        "categoria": "corporativo",
    },
    {
        "codigo": "testimonio",
        "nombre": "Testimonio / Resultado",
        "descripcion": "Tarjeta de resultado destacada, cita, atribución con avatar SVG.",
        "categoria": "narrativo",
    },
    {
        "codigo": "startup_saas",
        "nombre": "Startup SaaS",
        "descripcion": "Layout horizontal bicolor, headline gigante, badge flotante con métrica.",
        "categoria": "tech",
    },
    {
        "codigo": "tech_futurista",
        "nombre": "Tech Futurista",
        "descripcion": "Fondo oscuro con grid SVG, neon border, headline con efecto glitch.",
        "categoria": "tech",
    },
    {
        "codigo": "ia_neural",
        "nombre": "IA Neural",
        "descripcion": "Nodes SVG animados, gradiente cian-púrpura, headline IA centrado.",
        "categoria": "tech",
    },
    {
        "codigo": "dashboard_analytics",
        "nombre": "Dashboard Analytics",
        "descripcion": "Mockup de panel con 4 KPI cards y mini sparkline SVG.",
        "categoria": "corporativo",
    },
    {
        "codigo": "modern_gradient",
        "nombre": "Modern Gradient",
        "descripcion": "Gradiente diagonal vibrante, texto blanco en capas, patrón de puntos.",
        "categoria": "editorial",
    },
    # ── HISTORIA (5 estilos) ───────────────────────────────────────────────
    {
        "codigo": "historia_encuesta",
        "nombre": "Historia · Encuesta",
        "descripcion": "Pantalla de pregunta con sticker de encuesta interactiva.",
        "categoria": "narrativo",
    },
    {
        "codigo": "historia_quiz",
        "nombre": "Historia · Quiz",
        "descripcion": "3 opciones de respuesta con fondo de color y progress bar.",
        "categoria": "educativo",
    },
    {
        "codigo": "historia_antes_despues",
        "nombre": "Historia · Antes/Después",
        "descripcion": "Pantalla dividida antes vs después con slider SVG central.",
        "categoria": "narrativo",
    },
    {
        "codigo": "historia_cta_urgente",
        "nombre": "Historia · CTA Urgente",
        "descripcion": "Countdown SVG, headline de urgencia, botón CTA grande.",
        "categoria": "corporativo",
    },
    {
        "codigo": "historia_detras_camaras",
        "nombre": "Historia · Detrás de Cámaras",
        "descripcion": "Estética de video raw, texto informal, sticker de proceso.",
        "categoria": "narrativo",
    },
    # ── CARRUSEL (5 estilos) ───────────────────────────────────────────────
    {
        "codigo": "carrusel_problema_solucion",
        "nombre": "Carrusel · Problema/Solución",
        "descripcion": "6 slides: portada → problema → consecuencia → solución → beneficio → CTA.",
        "categoria": "narrativo",
    },
    {
        "codigo": "carrusel_lista_numerada",
        "nombre": "Carrusel · Lista Numerada",
        "descripcion": "Número grande en cada slide, jerarquía clara, progreso visual.",
        "categoria": "educativo",
    },
    {
        "codigo": "carrusel_caso_exito",
        "nombre": "Carrusel · Caso de Éxito",
        "descripcion": "Historia de cliente: contexto → desafío → solución → resultado → CTA.",
        "categoria": "narrativo",
    },
    {
        "codigo": "carrusel_tutorial",
        "nombre": "Carrusel · Tutorial Pasos",
        "descripcion": "Cada slide es un paso numerado con ícono SVG y descripción concisa.",
        "categoria": "educativo",
    },
    {
        "codigo": "carrusel_mitos_realidad",
        "nombre": "Carrusel · Mitos vs Realidad",
        "descripcion": "Slides alternados mito (rojo) vs realidad (verde), icono ✗/✓.",
        "categoria": "educativo",
    },
    # ── REEL (5 estilos) ──────────────────────────────────────────────────
    {
        "codigo": "reel_hook_solucion",
        "nombre": "Reel · Hook + Solución",
        "descripcion": "5 escenas: hook impactante → problema → solución → beneficio → CTA.",
        "categoria": "narrativo",
    },
    {
        "codigo": "reel_caso_exito",
        "nombre": "Reel · Caso de Éxito",
        "descripcion": "Storyboard de resultado real: antes → proceso → resultado + número.",
        "categoria": "narrativo",
    },
    {
        "codigo": "reel_tutorial_rapido",
        "nombre": "Reel · Tutorial Rápido",
        "descripcion": "Pasos numerados superpuestos, duración 30 s, texto en pantalla grande.",
        "categoria": "educativo",
    },
    {
        "codigo": "reel_error_comun",
        "nombre": "Reel · Error Común",
        "descripcion": "Hook de error → consecuencia → corrección → tip → CTA.",
        "categoria": "educativo",
    },
    {
        "codigo": "reel_tendencia_educativa",
        "nombre": "Reel · Tendencia Educativa",
        "descripcion": "Dato trending → contexto → opinión → acción. Estética editorial.",
        "categoria": "educativo",
    },
]


class Command(BaseCommand):
    help = "Puebla la tabla EstiloVisualInstagram con el catálogo base de 25 estilos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina todos los estilos existentes antes de insertar.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted, _ = EstiloVisualInstagram.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Eliminados {deleted} estilos previos."))

        creados = actualizados = 0
        for datos in ESTILOS:
            obj, created = EstiloVisualInstagram.objects.update_or_create(
                codigo=datos["codigo"],
                defaults={
                    "nombre":      datos["nombre"],
                    "descripcion": datos["descripcion"],
                    "categoria":   datos["categoria"],
                    "activo":      True,
                },
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"seed_estilos completado: {creados} creados, {actualizados} actualizados. "
                f"Total: {EstiloVisualInstagram.objects.count()} estilos activos."
            )
        )
