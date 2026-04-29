from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Workspace


class ConvertDemoRequestForm(forms.Form):
    workspace = forms.ModelChoiceField(
        queryset=Workspace.objects.all().order_by("name"),
        required=True,
        label="Workspace destino",
    )

    assigned_to = forms.ModelChoiceField(
        queryset=get_user_model().objects.all().order_by("email"),
        required=False,
        label="Ejecutivo asignado (opcional)",
    )

    stage = forms.CharField(
        required=False,
        max_length=80,
        label="Etapa (opcional)",
        help_text="Si tu modelo Lead maneja etapas por un campo string (ej: 'new', 'contacted').",
    )