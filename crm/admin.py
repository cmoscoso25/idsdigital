from django.contrib import admin
from .models import Lead, LeadNote, LeadAuditLog

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "nombre", "email", "empresa", "estado", "owner", "fecha_creacion")
    list_filter = ("workspace", "estado")
    search_fields = ("nombre", "email", "empresa", "asunto")
    autocomplete_fields = ("owner",)

@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ("lead", "author", "created_at")
    search_fields = ("lead__email", "lead__nombre", "content")

@admin.register(LeadAuditLog)
class LeadAuditLogAdmin(admin.ModelAdmin):
    list_display = ("lead", "workspace", "actor", "action", "created_at")
    list_filter = ("workspace", "action")
    search_fields = ("lead__email", "lead__nombre", "message")