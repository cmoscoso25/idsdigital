from django import forms
from django.core.exceptions import ValidationError

from .models import Lead, LeadNote


class LeadStageForm(forms.Form):
    """
    Form simple para cambiar etapa (no requiere ModelForm).
    views.py espera:
      - form.is_valid()
      - form.cleaned_data["estado"]
    """
    estado = forms.ChoiceField(choices=Lead.Stage.choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX / UI: usar tu estilo .input
        self.fields["estado"].widget.attrs.update({
            "class": "input",
        })


class LeadNoteForm(forms.ModelForm):
    """
    Nota interna del lead.

    Importante: anticipamos variaciones del nombre del campo en el modelo LeadNote.
    Tu views.py hace:
      note = form.save(commit=False)
      note.lead = lead
      note.author = request.user
      note.save()

    Para no romper si el campo no se llama 'texto', declaramos un field de formulario
    neutro ('texto') y en save() lo mapeamos al primer campo compatible del modelo.
    """
    texto = forms.CharField(
        label="Nota",
        required=True,
        widget=forms.Textarea(attrs={
            "class": "input",
            "rows": 3,
            "placeholder": "Escribe una nota interna…",
        })
    )

    class Meta:
        model = LeadNote
        fields = []  # usamos el field declarado arriba

    def save(self, commit=True):
        instance = super().save(commit=False)

        value = (self.cleaned_data.get("texto") or "").strip()

        # Mapeo robusto al campo real del modelo (anticipación de errores)
        possible_fields = ("texto", "mensaje", "nota", "contenido", "body", "content", "descripcion", "detalle")
        target = None
        for name in possible_fields:
            if hasattr(instance, name):
                target = name
                break

        if not target:
            # Si tu modelo LeadNote tiene otro nombre, aquí te dirá exactamente qué pasa.
            raise ValidationError(
                "No se encontró un campo de texto compatible en LeadNote. "
                "Ajusta LeadNoteForm.save() para mapear al nombre real del campo."
            )

        setattr(instance, target, value)

        if commit:
            instance.save()

        return instance


class LeadCreateForm(forms.ModelForm):
    """
    Formulario de creación manual de leads (panel).

    ✔ Multi-tenant: valida duplicados por (workspace, email)
    ✔ Guarda referencia del lead existente para UX (self.existing_lead)
    ✔ UX:
      - aplica clases UI correctas (.input y .form-input)
      - autofocus en nombre en GET
      - autofocus en email si hay duplicado/error
    """

    def __init__(self, *args, workspace=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace = workspace
        self.existing_lead = None

        # Alinear estilos a tu CSS: .input (principal) + .form-input (compat)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs.update({
                "class": (existing_class + " input form-input").strip(),
                "autocomplete": "off",
            })

        # Autofocus inicial (GET) en nombre para acelerar ingreso
        if "nombre" in self.fields:
            self.fields["nombre"].widget.attrs.setdefault("autofocus", True)

    class Meta:
        model = Lead
        fields = [
            "nombre",
            "email",
            "telefono",
            "empresa",
            "asunto",
            "mensaje",
        ]

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            return email

        if not self.workspace:
            raise ValidationError("No se pudo determinar el workspace actual.")

        qs = Lead.objects.filter(workspace=self.workspace, email__iexact=email)

        # Creación
        if not getattr(self.instance, "pk", None):
            existing = qs.first()
            if existing:
                self.existing_lead = existing

                # UX enterprise: llevar foco a email y marcar inválido
                self.fields["email"].widget.attrs["autofocus"] = True
                self.fields["email"].widget.attrs["aria-invalid"] = "true"

                raise ValidationError("Ya existe un lead con este email en este workspace.")

        # Edición (por si reusas el form en el futuro)
        else:
            existing = qs.exclude(pk=self.instance.pk).first()
            if existing:
                self.existing_lead = existing
                self.fields["email"].widget.attrs["autofocus"] = True
                self.fields["email"].widget.attrs["aria-invalid"] = "true"
                raise ValidationError("Ya existe otro lead con este email en este workspace.")

        return email