from django.db import models
from django.conf import settings
from django.utils import timezone

from accounts.models import Workspace


class Lead(models.Model):
    class Stage(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        EN_GESTION = "en_gestion", "En gestión"
        COTIZADO = "cotizado", "Cotizado"
        CERRADO = "cerrado", "Cerrado"
        PERDIDO = "perdido", "Perdido"

    # ✅ Enterprise: NOT NULL (tenant isolation real)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="leads",
        help_text="Empresa/Workspace dueño del lead (tenant).",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_leads",
        help_text="Ejecutivo asignado al lead.",
    )

    # ✅ Enterprise: NOT NULL
    nombre = models.CharField(
        max_length=120,
        help_text="Nombre del contacto.",
    )

    email = models.EmailField()
    telefono = models.CharField(max_length=40, blank=True)
    empresa = models.CharField(max_length=160, blank=True)

    asunto = models.CharField(max_length=160, blank=True)
    mensaje = models.TextField(blank=True)

    estado = models.CharField(
        max_length=24,
        choices=Stage.choices,
        default=Stage.NUEVO,
        db_index=True,
    )

    fecha_creacion = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-fecha_creacion",)
        indexes = [
            # filtros típicos del CRM
            models.Index(fields=["workspace", "estado", "fecha_creacion"]),
            models.Index(fields=["workspace", "updated_at"]),
            models.Index(fields=["workspace", "email"]),
            models.Index(fields=["workspace", "empresa"]),
            models.Index(fields=["workspace", "owner"]),
        ]
        constraints = [
            # Evita duplicados "obvios" por tenant (ajustable)
            models.UniqueConstraint(
                fields=["workspace", "email"],
                name="uniq_lead_email_per_workspace",
            )
        ]

    def __str__(self) -> str:
        return f"{self.nombre} - {self.email} ({self.get_estado_display()})"


class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lead_notes",
    )

    # ✅ Enterprise: NOT NULL
    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["lead", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"Nota Lead #{self.lead_id}"


class LeadAuditLog(models.Model):
    """
    Auditoría simple y útil:
    - qué pasó (action)
    - actor (user)
    - lead
    - before/after JSON para cambios clave
    """

    class Action(models.TextChoices):
        CREATED = "created", "Creado"
        STAGE_CHANGED = "stage_changed", "Cambio de etapa"
        OWNER_CHANGED = "owner_changed", "Reasignación"
        NOTE_ADDED = "note_added", "Nota agregada"
        UPDATED = "updated", "Actualización"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="audit_logs")

    # ✅ Enterprise: NOT NULL y related_name único (sin choque con workspace.leads)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="audit_logs",
        help_text="Workspace relacionado al evento (tenant).",
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lead_audit_events",
    )

    action = models.CharField(max_length=40, choices=Action.choices, db_index=True)
    message = models.CharField(max_length=240, blank=True)

    before = models.JSONField(default=dict, blank=True)
    after = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["workspace", "created_at"]),
            models.Index(fields=["lead", "created_at"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_action_display()} Lead #{self.lead_id}"