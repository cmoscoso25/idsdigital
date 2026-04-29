from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    User corporativo (extensible). No guardamos tenant aquí para permitir multi-workspace.
    """
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Workspace(models.Model):
    """
    Tenant simple (empresa/unidad). Base para SaaS multi-tenant real.
    """
    name = models.CharField(max_length=160)
    legal_name = models.CharField(max_length=220, blank=True)
    rut = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class Membership(models.Model):
    """
    Vincula usuario a workspace + rol (RBAC).
    """
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        SUPERVISOR = "supervisor", "Supervisor"
        SALES = "sales", "Comercial"
        READONLY = "readonly", "Solo lectura"

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="memberships")
    workspace = models.ForeignKey("accounts.Workspace", on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=24, choices=Role.choices, default=Role.SALES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "workspace")
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"

    def __str__(self) -> str:
        return f"{self.user.username} @ {self.workspace.name} ({self.role})"