from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    STARTER = "starter"
    PRO = "pro"
    AGENCY = "agency"
    TIER_CHOICES = [
        (STARTER, "Starter"),
        (PRO, "Pro"),
        (AGENCY, "Agency"),
    ]

    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    nombre = models.CharField(max_length=60)
    precio_usd = models.DecimalField(max_digits=6, decimal_places=2)
    posts_por_mes = models.PositiveIntegerField(help_text="Límite de contenidos generados por mes")
    stripe_price_id = models.CharField(max_length=100, blank=True, help_text="price_xxx de Stripe")
    activo = models.BooleanField(default=True)
    orden = models.PositiveSmallIntegerField(default=0, help_text="Orden de presentación en pricing")

    class Meta:
        ordering = ["orden"]
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return f"{self.nombre} (${self.precio_usd}/mes)"


class Subscription(models.Model):
    TRIAL = "trial"
    ACTIVO = "activo"
    CANCELADO = "cancelado"
    VENCIDO = "vencido"
    PAGO_FALLIDO = "pago_fallido"
    ESTADO_CHOICES = [
        (TRIAL, "Trial"),
        (ACTIVO, "Activo"),
        (CANCELADO, "Cancelado"),
        (VENCIDO, "Vencido"),
        (PAGO_FALLIDO, "Pago fallido"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscriptions",
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=TRIAL)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    trial_fin = models.DateTimeField(null=True, blank=True)
    periodo_actual_fin = models.DateTimeField(null=True, blank=True)
    posts_generados_mes = models.PositiveIntegerField(default=0)
    posts_reset_fecha = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        plan_nombre = self.plan.nombre if self.plan else "Sin plan"
        return f"{self.usuario.email} — {plan_nombre} ({self.get_estado_display()})"

    @property
    def esta_activa(self):
        if self.estado == self.ACTIVO:
            return True
        if self.estado == self.TRIAL and self.trial_fin and self.trial_fin > timezone.now():
            return True
        return False

    @property
    def posts_disponibles(self):
        limite = self._limite_posts()
        return max(0, limite - self.posts_generados_mes)

    @property
    def puede_generar(self):
        return self.esta_activa and self.posts_disponibles > 0

    @property
    def limite_posts(self):
        if self.estado == self.TRIAL:
            return 10
        if self.plan:
            return self.plan.posts_por_mes
        return 0

    def _limite_posts(self):
        return self.limite_posts

    def registrar_generacion(self):
        """Incrementa el contador; resetea si el mes cambió."""
        hoy = timezone.now().date()
        if (
            not self.posts_reset_fecha
            or hoy.month != self.posts_reset_fecha.month
            or hoy.year != self.posts_reset_fecha.year
        ):
            self.posts_generados_mes = 0
            self.posts_reset_fecha = hoy
        self.posts_generados_mes += 1
        self.save(update_fields=["posts_generados_mes", "posts_reset_fecha"])
