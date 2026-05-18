from django.conf import settings
from django.db import models
from django.utils.text import slugify


class DemoRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Nueva"
        IN_REVIEW = "in_review", "En revisión"
        CONTACTED = "contacted", "Contactado"
        QUALIFIED = "qualified", "Calificado"
        DISCARDED = "discarded", "Descartado"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Datos del formulario
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=160, blank=True)
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField(blank=True)

    # Trazabilidad / control
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    internal_notes = models.TextField(blank=True)

    # Auditoría leve
    submitted_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    # Conversión
    converted_to_lead = models.BooleanField(default=False)
    converted_at = models.DateTimeField(null=True, blank=True)

    # Quien gestionó la solicitud (usuario interno)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="handled_demo_requests",
    )

    # Lead creado (en tenant)
    lead = models.ForeignKey(
        "crm.Lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="demo_requests",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.company or 'Sin empresa'} - {self.email}"


class BlogPost(models.Model):
    # Datos principales
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Resumen corto para listado y SEO")
    content = models.TextField(help_text="Contenido completo del artículo en HTML")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True, help_text="Título SEO (máx 70 caracteres)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Descripción SEO (máx 160 caracteres)")
    meta_keywords = models.CharField(max_length=300, blank=True)

    # Categoría simple
    category = models.CharField(max_length=80, blank=True, help_text="Ej: Automatización, Software, IA")

    # Control de publicación
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False, help_text="Destacar en la landing")

    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["published", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        # Genera el slug automáticamente desde el título si no existe
        if not self.slug:
            self.slug = slugify(self.title)
        # Usa el título como meta_title si no se especificó
        if not self.meta_title:
            self.meta_title = self.title[:70]
        # Usa el excerpt como meta_description si no se especificó
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title