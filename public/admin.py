from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils import timezone

from .admin_forms import ConvertDemoRequestForm
from .models import DemoRequest, BlogPost

from crm.models import Lead


def _safe_set(instance, field_name: str, value):
    """
    Setea un campo si existe en el modelo.
    Retorna True si se seteó, False si no existe.
    """
    if hasattr(instance, field_name):
        setattr(instance, field_name, value)
        return True
    return False


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "company", "name", "email", "phone", "converted_to_lead")
    list_filter = ("status", "converted_to_lead", "created_at")
    search_fields = ("email", "company", "name", "phone", "subject")
    readonly_fields = ("created_at", "updated_at", "submitted_ip", "user_agent", "converted_at")

    change_form_template = "admin/public/demorequest/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:object_id>/convert/",
                self.admin_site.admin_view(self.convert_view),
                name="public_demorequest_convert",
            ),
        ]
        return custom + urls

    def convert_view(self, request, object_id: int):
        demo = get_object_or_404(DemoRequest, pk=object_id)

        if demo.converted_to_lead and demo.lead_id:
            self.message_user(request, "Esta solicitud ya fue convertida a Lead.", level=messages.INFO)
            return redirect(f"../{demo.pk}/change/")

        if request.method == "POST":
            form = ConvertDemoRequestForm(request.POST)
            if form.is_valid():
                workspace = form.cleaned_data["workspace"]
                assigned_to = form.cleaned_data.get("assigned_to")
                stage = (form.cleaned_data.get("stage") or "").strip()

                lead = Lead()

                if not _safe_set(lead, "workspace", workspace):
                    self.message_user(
                        request,
                        "ERROR: Lead no tiene campo 'workspace'. Revisa crm.models.Lead.",
                        level=messages.ERROR,
                    )
                    return redirect(f"../{demo.pk}/change/")

                if not (_safe_set(lead, "name", demo.name) or _safe_set(lead, "full_name", demo.name) or _safe_set(lead, "contact_name", demo.name)):
                    pass

                if not (_safe_set(lead, "email", demo.email) or _safe_set(lead, "contact_email", demo.email)):
                    pass

                if demo.phone:
                    _safe_set(lead, "phone", demo.phone) or _safe_set(lead, "contact_phone", demo.phone)

                if demo.company:
                    _safe_set(lead, "company", demo.company) or _safe_set(lead, "company_name", demo.company) or _safe_set(lead, "organization", demo.company)

                if demo.subject:
                    _safe_set(lead, "title", demo.subject) or _safe_set(lead, "subject", demo.subject)

                if demo.message:
                    _safe_set(lead, "description", demo.message) or _safe_set(lead, "details", demo.message)

                if assigned_to:
                    _safe_set(lead, "assigned_to", assigned_to) or _safe_set(lead, "owner", assigned_to) or _safe_set(lead, "executive", assigned_to)

                if stage:
                    _safe_set(lead, "stage", stage) or _safe_set(lead, "status", stage)

                try:
                    lead.save()
                except Exception as e:
                    self.message_user(
                        request,
                        f"ERROR al crear Lead: {e}",
                        level=messages.ERROR,
                    )
                    return redirect(f"../{demo.pk}/change/")

                demo.converted_to_lead = True
                demo.converted_at = timezone.now()
                demo.handled_by = request.user
                demo.lead = lead
                demo.status = DemoRequest.Status.QUALIFIED
                demo.save(update_fields=["converted_to_lead", "converted_at", "handled_by", "lead", "status", "updated_at"])

                self.message_user(request, "✅ Solicitud convertida a Lead correctamente.", level=messages.SUCCESS)

                try:
                    lead_url = reverse("admin:crm_lead_change", args=[lead.pk])
                    return redirect(lead_url)
                except Exception:
                    return redirect(f"../{demo.pk}/change/")

        else:
            form = ConvertDemoRequestForm()

        context = dict(
            self.admin_site.each_context(request),
            title="Convertir solicitud a Lead",
            demo=demo,
            form=form,
        )
        return render(request, "admin/public/demorequest/convert.html", context)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published", "featured", "published_at", "created_at")
    list_filter = ("published", "featured", "category")
    search_fields = ("title", "excerpt", "content", "meta_keywords")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Contenido", {
            "fields": ("title", "slug", "excerpt", "content", "category")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "classes": ("collapse",),
        }),
        ("Publicación", {
            "fields": ("published", "featured", "published_at")
        }),
        ("Auditoría", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )