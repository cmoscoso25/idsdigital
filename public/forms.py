from django import forms


class DemoRequestForm(forms.Form):
    nombre = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)

    # El selector reemplaza visualmente al campo asunto
    necesidad = forms.ChoiceField(
        required=False,
        choices=[
            ("", "¿Qué necesitas resolver?"),
            ("Software a medida", "Software a medida"),
            ("Automatización de procesos", "Automatización de procesos"),
            ("Inteligencia artificial", "Inteligencia artificial"),
            ("Dashboard / reportes", "Dashboard / reportes"),
            ("Integración de plataformas", "Integración de plataformas"),
            ("Otro", "Otro"),
        ]
    )

    # Estos campos siguen existiendo para no romper el CRM
    # Se envían vacíos desde el formulario simplificado
    telefono = forms.CharField(max_length=40, required=False)
    empresa = forms.CharField(max_length=160, required=False)
    asunto = forms.CharField(max_length=160, required=False)
    mensaje = forms.CharField(required=False, widget=forms.Textarea)

    # Honeypot anti-bots (debe venir vacío)
    website = forms.CharField(required=False)

    def clean_website(self):
        value = (self.cleaned_data.get("website") or "").strip()
        if value:
            raise forms.ValidationError("Bot detected.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        # Pasamos el valor del selector al campo asunto
        # para que el CRM lo reciba normalmente
        necesidad = cleaned_data.get("necesidad") or ""
        if necesidad:
            cleaned_data["asunto"] = necesidad
        return cleaned_data