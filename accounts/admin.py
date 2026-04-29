from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Workspace, Membership

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("name", "legal_name", "rut", "email", "phone", "created_at")
    search_fields = ("name", "legal_name", "rut", "email")

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "workspace", "role", "is_active", "created_at")
    list_filter = ("role", "is_active", "workspace")
    search_fields = ("user__username", "user__email", "workspace__name")