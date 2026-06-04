from django import forms
from .models import EmpresaNexa, MemoriaMarca, ContenidoGenerado


class EmpresaNexaForm(forms.ModelForm):
    class Meta:
        model = EmpresaNexa
        exclude = ["usuario", "fecha_creacion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "publico_objetivo": forms.Textarea(attrs={"rows": 3}),
            "color_principal": forms.TextInput(attrs={"type": "color", "class": "nxa-color-input"}),
            "color_secundario": forms.TextInput(attrs={"type": "color", "class": "nxa-color-input"}),
        }


class MemoriaMarcaForm(forms.ModelForm):
    class Meta:
        model = MemoriaMarca
        exclude = ["empresa"]
        widgets = {
            "propuesta_valor": forms.Textarea(attrs={"rows": 3}),
            "servicios_principales": forms.Textarea(attrs={"rows": 4}),
            "palabras_clave": forms.Textarea(attrs={"rows": 2}),
            "estilo_comunicacion": forms.Textarea(attrs={"rows": 3}),
            "evitar_mencionar": forms.Textarea(attrs={"rows": 2}),
            "instrucciones_ia": forms.Textarea(attrs={"rows": 3}),
            "resumen_marca": forms.Textarea(attrs={"rows": 4}),
        }


class GenerarContenidoForm(forms.Form):
    tipo_contenido = forms.ChoiceField(
        choices=ContenidoGenerado.TIPOS,
        label="Tipo de contenido",
    )
    objetivo = forms.CharField(
        max_length=200,
        label="Objetivo del contenido",
        widget=forms.TextInput(attrs={"placeholder": "ej: aumentar seguidores, lanzar producto"}),
    )
    tema = forms.CharField(
        max_length=300,
        label="Tema o producto a destacar",
        widget=forms.TextInput(attrs={"placeholder": "ej: nuestro servicio de diseño web"}),
    )
