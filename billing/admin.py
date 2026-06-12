from django.contrib import admin
from billing.models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tier", "precio_usd", "posts_por_mes", "stripe_price_id", "activo", "orden"]
    list_editable = ["activo", "orden", "stripe_price_id"]
    ordering = ["orden"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["usuario", "plan", "estado", "posts_generados_mes", "posts_reset_fecha", "trial_fin", "periodo_actual_fin"]
    list_filter = ["estado", "plan"]
    search_fields = ["usuario__email", "stripe_customer_id", "stripe_subscription_id"]
    readonly_fields = ["fecha_creacion", "fecha_actualizacion"]
