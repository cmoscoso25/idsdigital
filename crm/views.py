from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from crm.models import Lead

# Import seguro del modelo DemoRequest
try:
    from public.models import DemoRequest
except Exception:
    DemoRequest = None


# ==========================================
# HELPERS
# ==========================================
def _ensure_demorequest_model():
    if DemoRequest is None:
        raise Http404("DemoRequest no disponible. Revisa import public.models.DemoRequest.")


def _dr_attr(obj, *names, default=""):
    """
    Devuelve el primer atributo existente/no vacío.
    Soporta compatibilidad entre campos en español e inglés.
    """
    for name in names:
        if hasattr(obj, name):
            value = getattr(obj, name)
            if value not in (None, ""):
                return value
    return default


def _get_demorequest_status_label(obj) -> str:
    status = _dr_attr(obj, "status", default="")
    if status:
        status_str = str(status).strip().lower()

        if status_str in ("new", "nueva"):
            return "Nueva"
        if status_str in ("in_review", "en revisión", "en revision"):
            return "En revisión"
        if status_str in ("contacted", "contactado"):
            return "Contactado"
        if status_str in ("qualified", "calificado"):
            return "Convertida"
        if status_str in ("discarded", "descartado"):
            return "Archivada"
        if status_str in ("convertida", "converted", "converted_to_lead"):
            return "Convertida"
        if status_str in ("archivada", "archived"):
            return "Archivada"

        return str(status)

    if hasattr(obj, "converted_to_lead") and getattr(obj, "converted_to_lead", False):
        return "Convertida"

    if hasattr(obj, "lead") and getattr(obj, "lead", None):
        return "Convertida"

    if hasattr(obj, "converted_at") and getattr(obj, "converted_at", None):
        return "Convertida"

    if hasattr(obj, "is_archived") and getattr(obj, "is_archived", False):
        return "Archivada"

    if hasattr(obj, "archived") and getattr(obj, "archived", False):
        return "Archivada"

    if hasattr(obj, "archived_at") and getattr(obj, "archived_at", None):
        return "Archivada"

    return "Nueva"


def _is_demorequest_converted(obj) -> bool:
    if hasattr(obj, "converted_to_lead") and getattr(obj, "converted_to_lead", False):
        return True
    if hasattr(obj, "lead") and getattr(obj, "lead", None):
        return True
    if hasattr(obj, "converted_at") and getattr(obj, "converted_at", None):
        return True

    return "convert" in _get_demorequest_status_label(obj).lower()


def _is_demorequest_archived(obj) -> bool:
    return "archiv" in _get_demorequest_status_label(obj).lower()


def _demorequest_created_value(obj):
    if hasattr(obj, "created_at") and getattr(obj, "created_at", None):
        return obj.created_at
    if hasattr(obj, "created") and getattr(obj, "created", None):
        return obj.created
    return None


def _normalize_demorequest_row(obj):
    return {
        "obj": obj,
        "label": _get_demorequest_status_label(obj),
        "is_converted": _is_demorequest_converted(obj),
        "is_archived": _is_demorequest_archived(obj),
        "nombre": _dr_attr(obj, "nombre", "name", default=""),
        "email": _dr_attr(obj, "email", default=""),
        "telefono": _dr_attr(obj, "telefono", "phone", default=""),
        "empresa": _dr_attr(obj, "empresa", "company", default=""),
        "asunto": _dr_attr(obj, "asunto", "subject", default=""),
        "mensaje": _dr_attr(obj, "mensaje", "message", default=""),
        "fecha": _demorequest_created_value(obj),
    }


# ==========================================
# CRM - LEADS
# ==========================================
@login_required
def lead_list(request):
    if not request.workspace:
        return redirect("accounts:workspace_select")
    qs = Lead.objects.filter(workspace=request.workspace).order_by("-fecha_creacion", "-id")
    return render(request, "crm/lead_list.html", {"leads": qs})


@login_required
def lead_detail(request, lead_id):
    if not request.workspace:
        return redirect("accounts:workspace_select")
    lead = get_object_or_404(Lead, id=lead_id, workspace=request.workspace)
    return render(request, "crm/lead_detail.html", {"lead": lead})


@login_required
@require_POST
def lead_change_status(request, lead_id):
    if not request.workspace:
        return redirect("accounts:workspace_select")
    lead = get_object_or_404(Lead, id=lead_id, workspace=request.workspace)
    nuevo_estado = (request.POST.get("estado") or "").strip()

    estados_validos = {
        "nuevo",
        "en_gestion",
        "cotizado",
        "cerrado",
        "perdido",
    }

    if nuevo_estado in estados_validos:
        lead.estado = nuevo_estado
        lead.save(update_fields=["estado", "updated_at"])
        messages.success(request, f"Lead #{lead.id} actualizado a '{lead.get_estado_display()}'.")
    else:
        messages.warning(request, "No se pudo actualizar el estado del lead.")

    return redirect("crm:lead_list")


# ==========================================
# CRM - SOLICITUDES
# ==========================================
@login_required
def demorequest_list(request):
    _ensure_demorequest_model()

    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "todas").strip().lower()

    qs = DemoRequest.objects.all()

    if status != "archivadas":
        if hasattr(DemoRequest, "is_archived"):
            qs = qs.filter(is_archived=False)
        elif hasattr(DemoRequest, "archived"):
            qs = qs.filter(archived=False)

    raw = list(qs)

    if q:
        q_lower = q.lower()
        filtradas = []
        for r in raw:
            nombre = str(_dr_attr(r, "nombre", "name", default="")).lower()
            email = str(_dr_attr(r, "email", default="")).lower()
            telefono = str(_dr_attr(r, "telefono", "phone", default="")).lower()
            empresa = str(_dr_attr(r, "empresa", "company", default="")).lower()
            asunto = str(_dr_attr(r, "asunto", "subject", default="")).lower()
            mensaje = str(_dr_attr(r, "mensaje", "message", default="")).lower()

            if (
                q_lower in nombre
                or q_lower in email
                or q_lower in telefono
                or q_lower in empresa
                or q_lower in asunto
                or q_lower in mensaje
            ):
                filtradas.append(r)
        raw = filtradas

    def _sort_key(item):
        fecha = _demorequest_created_value(item)
        if fecha:
            return fecha
        return timezone.now()

    raw = sorted(raw, key=_sort_key, reverse=True)

    rows = [_normalize_demorequest_row(r) for r in raw]

    if status == "nuevas":
        rows = [r for r in rows if (not r["is_converted"] and not r["is_archived"])]
    elif status == "convertidas":
        rows = [r for r in rows if r["is_converted"]]
    elif status == "archivadas":
        rows = [r for r in rows if r["is_archived"]]

    kpi_total = len(rows)
    kpi_nuevas = sum(1 for x in rows if (not x["is_converted"] and not x["is_archived"]))
    kpi_convertidas = sum(1 for x in rows if x["is_converted"])
    kpi_archivadas = sum(1 for x in rows if x["is_archived"])

    context = {
        "requests": rows,
        "q": q,
        "status": status,
        "kpi_total": kpi_total,
        "kpi_nuevas": kpi_nuevas,
        "kpi_convertidas": kpi_convertidas,
        "kpi_archivadas": kpi_archivadas,
    }
    return render(request, "crm/demorequest_list.html", context)


@login_required
def demorequest_detail(request, request_id):
    _ensure_demorequest_model()
    obj = get_object_or_404(DemoRequest, id=request_id)

    context = {
        "req": obj,
        "req_data": _normalize_demorequest_row(obj),
        "status_label": _get_demorequest_status_label(obj),
        "is_converted": _is_demorequest_converted(obj),
        "is_archived": _is_demorequest_archived(obj),
    }
    return render(request, "crm/demorequest_detail.html", context)


@login_required
@require_POST
@transaction.atomic
def demorequest_convert(request, request_id):
    _ensure_demorequest_model()
    obj = get_object_or_404(DemoRequest, id=request_id)

    if _is_demorequest_converted(obj):
        messages.info(request, "Esta solicitud ya está convertida.")
        return redirect("crm:demorequest_detail", request_id=obj.id)

    nombre = _dr_attr(obj, "nombre", "name", default="")
    email = _dr_attr(obj, "email", default="")
    telefono = _dr_attr(obj, "telefono", "phone", default="")
    empresa = _dr_attr(obj, "empresa", "company", default="")
    asunto = _dr_attr(obj, "asunto", "subject", default="")
    mensaje = _dr_attr(obj, "mensaje", "message", default="")

    lead = Lead()

    if hasattr(lead, "nombre"):
        lead.nombre = nombre
    elif hasattr(lead, "name"):
        lead.name = nombre

    if hasattr(lead, "email"):
        lead.email = email

    if hasattr(lead, "empresa"):
        lead.empresa = empresa
    elif hasattr(lead, "company"):
        lead.company = empresa
    elif hasattr(lead, "company_name"):
        lead.company_name = empresa

    lead.estado = "nuevo"

    if hasattr(lead, "owner"):
        lead.owner = request.user
    elif hasattr(lead, "created_by"):
        lead.created_by = request.user

    if request.workspace is not None and hasattr(lead, "workspace"):
        lead.workspace = request.workspace

    if hasattr(lead, "telefono"):
        lead.telefono = telefono
    elif hasattr(lead, "phone"):
        lead.phone = telefono

    if hasattr(lead, "asunto"):
        lead.asunto = asunto
    elif hasattr(lead, "subject"):
        lead.subject = asunto

    if hasattr(lead, "mensaje"):
        lead.mensaje = mensaje
    elif hasattr(lead, "message"):
        lead.message = mensaje

    lead.save()

    now = timezone.now()

    if hasattr(obj, "status"):
        try:
            obj.status = "qualified"
        except Exception:
            pass

    if hasattr(obj, "converted_at"):
        obj.converted_at = now

    if hasattr(obj, "converted_to_lead"):
        obj.converted_to_lead = True

    if hasattr(obj, "lead"):
        try:
            obj.lead = lead
        except Exception:
            pass

    obj.save()

    messages.success(request, f"Solicitud convertida a Lead (ID #{lead.id}).")
    return redirect("crm:lead_detail", lead_id=lead.id)


@login_required
@require_POST
@transaction.atomic
def demorequest_archive(request, request_id):
    _ensure_demorequest_model()
    obj = get_object_or_404(DemoRequest, id=request_id)

    if _is_demorequest_archived(obj):
        messages.info(request, "Esta solicitud ya está archivada.")
        return redirect("crm:demorequest_detail", request_id=obj.id)

    changed = False

    if hasattr(obj, "is_archived"):
        obj.is_archived = True
        changed = True

    if hasattr(obj, "archived"):
        obj.archived = True
        changed = True

    if hasattr(obj, "status"):
        try:
            obj.status = "discarded"
            changed = True
        except Exception:
            pass

    if hasattr(obj, "archived_at"):
        obj.archived_at = timezone.now()
        changed = True

    if changed:
        obj.save()
        messages.success(request, "Solicitud archivada.")
    else:
        messages.warning(
            request,
            "No se pudo archivar porque DemoRequest no tiene campos de archivado (status/is_archived/archived).",
        )

    return redirect("crm:demorequest_list")