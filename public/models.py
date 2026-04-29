from django.conf import settings
from django.db import models


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