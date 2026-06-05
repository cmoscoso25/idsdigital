from django.db import models
from django.conf import settings


class EmpresaNexa(models.Model):
    TONOS = [
        ("profesional", "Profesional"),
        ("cercano", "Cercano y amigable"),
        ("inspirador", "Inspirador"),
        ("humoristico", "Humorístico"),
        ("exclusivo", "Exclusivo / Premium"),
        ("educativo", "Educativo"),
    ]
    OBJETIVOS = [
        ("ventas", "Aumentar ventas"),
        ("reconocimiento", "Reconocimiento de marca"),
        ("comunidad", "Construir comunidad"),
        ("educacion", "Educar al mercado"),
        ("confianza", "Generar confianza"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="empresas_nexa",
        help_text="Usuario propietario de esta empresa en Nexa",
    )
    nombre_empresa = models.CharField(max_length=200)
    rubro = models.CharField(max_length=200, help_text="Sector o industria de la empresa")
    descripcion = models.TextField(help_text="Descripción general del negocio")
    publico_objetivo = models.TextField(help_text="A quién va dirigida la empresa")
    tono_marca = models.CharField(max_length=50, choices=TONOS, default="profesional")
    objetivo_principal = models.CharField(max_length=50, choices=OBJETIVOS, default="ventas")
    instagram = models.CharField(
        max_length=100, blank=True, help_text="Usuario de Instagram sin @"
    )
    sitio_web = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to="nexa/logos/", blank=True, null=True,
        help_text="Logo de la empresa (PNG o JPG recomendado)",
    )
    color_principal = models.CharField(
        max_length=7, default="#3b82f6", help_text="Color hexadecimal principal, ej: #3b82f6"
    )
    color_secundario = models.CharField(
        max_length=7, default="#8b5cf6", help_text="Color hexadecimal secundario, ej: #8b5cf6"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empresa Nexa"
        verbose_name_plural = "Empresas Nexa"
        ordering = ["-fecha_creacion"]
        indexes = [models.Index(fields=["usuario"])]

    def __str__(self):
        return self.nombre_empresa


class MemoriaMarca(models.Model):
    empresa = models.OneToOneField(
        EmpresaNexa,
        on_delete=models.CASCADE,
        related_name="memoria_marca",
        help_text="Empresa a la que pertenece esta memoria de marca",
    )
    propuesta_valor = models.TextField(help_text="Qué hace única a esta empresa frente a la competencia")
    servicios_principales = models.TextField(help_text="Lista de servicios o productos principales, uno por línea")
    palabras_clave = models.TextField(help_text="Palabras clave de marca separadas por coma")
    estilo_comunicacion = models.TextField(help_text="Cómo se comunica la marca con su audiencia")
    evitar_mencionar = models.TextField(blank=True, help_text="Temas, palabras o frases que la marca NO debe usar")
    instrucciones_ia = models.TextField(
        blank=True, help_text="Instrucciones especiales para los agentes IA (contexto extra, restricciones)"
    )
    resumen_marca = models.TextField(
        blank=True, help_text="Resumen ejecutivo de la marca — generado o editado para uso en prompts IA"
    )

    class Meta:
        verbose_name = "Memoria de Marca"
        verbose_name_plural = "Memorias de Marca"

    def __str__(self):
        return f"Memoria: {self.empresa.nombre_empresa}"


class ContenidoGenerado(models.Model):
    TIPOS = [
        ("carrusel", "Carrusel"),
        ("historia", "Historia"),
        ("post", "Post"),
        ("reel", "Reel"),
        ("campana", "Campaña"),
    ]
    ESTADOS = [
        ("borrador", "Borrador"),
        ("aprobado", "Aprobado"),
        ("programado", "Programado"),
        ("publicado", "Publicado"),
    ]

    empresa = models.ForeignKey(
        EmpresaNexa,
        on_delete=models.CASCADE,
        related_name="contenidos",
        help_text="Empresa para la que se generó este contenido",
    )
    estrategia = models.ForeignKey(
        "EstrategiaMensual",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contenidos",
        help_text="Estrategia mensual que originó este contenido (opcional)",
    )
    tipo_contenido = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=300)
    copy = models.TextField(help_text="Texto principal del contenido")
    hashtags = models.TextField(blank=True, help_text="Hashtags separados por espacio")
    cta = models.CharField(max_length=200, blank=True, help_text="Call to action del contenido")
    estructura_json = models.JSONField(
        default=dict,
        help_text="Estructura detallada del contenido (diapositivas, escenas, stickers, etc.)",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    fecha_programada = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contenido Generado"
        verbose_name_plural = "Contenidos Generados"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["empresa", "estado"]),
            models.Index(fields=["fecha_creacion"]),
        ]

    def __str__(self):
        return f"{self.get_tipo_contenido_display()} — {self.titulo[:60]}"


class CreatividadInstagram(models.Model):
    TIPOS = [
        ("post",     "Post"),
        ("historia", "Historia"),
        ("carrusel", "Carrusel"),
        ("reel",     "Reel"),
    ]
    ESTADOS = [
        ("generada",  "Generada"),
        ("aprobada",  "Aprobada"),
        ("publicada", "Publicada"),
    ]

    contenido = models.ForeignKey(
        ContenidoGenerado,
        on_delete=models.CASCADE,
        related_name="creatividades",
        help_text="Contenido generado a partir del cual se creó esta creatividad",
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    prompt_visual = models.TextField(
        help_text="Prompt profesional listo para enviar a OpenAI Images / Flux / Ideogram / Gemini",
    )
    estructura_visual_json = models.JSONField(
        default=dict,
        help_text="Especificación visual completa: colores, slides, escenas, elementos de diseño",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="generada")
    render_html = models.TextField(
        blank=True,
        help_text="HTML renderizado del mockup — reemplazar por imagen real cuando se active la API de generación",
    )
    render_css = models.TextField(
        blank=True,
        help_text="CSS scoped del render — permite personalización por creatividad",
    )
    veces_regenerada = models.PositiveIntegerField(
        default=0,
        help_text="Número de veces que fue regenerada desde su creación inicial",
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Última vez que fue generada o regenerada — usado para anti-repetición de estilos",
    )
    estilo = models.CharField(
        max_length=50, blank=True, default="",
        help_text="ID del estilo creativo aplicado (corporate_kpi, minimalista_premium, etc.)",
    )
    estilo_nombre = models.CharField(
        max_length=100, blank=True, default="",
        help_text="Nombre legible del estilo creativo",
    )
    categoria_visual = models.CharField(
        max_length=30, blank=True, default="",
        help_text="Categoría temática detectada: software, ia, automatizacion, marketing, etc.",
    )
    imagen_generada = models.ImageField(
        upload_to="nexa/creatividades/",
        blank=True, null=True,
        help_text="Imagen real generada por IA (OpenAI DALL-E, Flux, Ideogram, Gemini). Si existe, reemplaza el mockup HTML.",
    )
    proveedor_ia = models.CharField(
        max_length=30, blank=True, default="",
        help_text="Proveedor usado para generar la imagen: openai, flux, ideogram, gemini",
    )
    fecha_generacion_imagen = models.DateTimeField(
        null=True, blank=True,
        help_text="Fecha y hora en que se generó la imagen IA",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Creatividad Instagram"
        verbose_name_plural = "Creatividades Instagram"
        ordering = ["-fecha_creacion"]
        indexes = [models.Index(fields=["contenido", "tipo"])]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.contenido.titulo[:50]}"


class EstrategiaMensual(models.Model):
    empresa = models.ForeignKey(
        EmpresaNexa,
        on_delete=models.CASCADE,
        related_name="estrategias",
        help_text="Empresa para la que se generó esta estrategia",
    )
    objetivo = models.TextField(help_text="Objetivo principal de la estrategia mensual")
    pilares_contenido = models.TextField(
        help_text="Pilares temáticos de contenido separados por coma"
    )
    frecuencia_publicacion = models.CharField(
        max_length=100,
        help_text="Frecuencia recomendada de publicación, ej: 3 veces por semana",
    )
    publico_objetivo = models.TextField(help_text="Público objetivo específico para este mes")
    calendario_json = models.JSONField(
        default=dict,
        help_text="Calendario semanal generado: 4 semanas con tipos y temas de contenido",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estrategia Mensual"
        verbose_name_plural = "Estrategias Mensuales"
        ordering = ["-fecha_creacion"]
        indexes = [models.Index(fields=["empresa"])]

    def __str__(self):
        return f"Estrategia {self.empresa.nombre_empresa} — {self.fecha_creacion.strftime('%m/%Y') if self.fecha_creacion else ''}"
