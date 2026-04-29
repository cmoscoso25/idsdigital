from django import forms


class DemoRequestForm(forms.Form):
    nombre = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=40, required=False)
    empresa = forms.CharField(max_length=160, required=False)
    asunto = forms.CharField(max_length=160, required=False)
    mensaje = forms.CharField(required=False, widget=forms.Textarea)

    # Honeypot anti-bots (debe venir vacío)
    website = forms.CharField(required=False)

    def clean_website(self):
        value = (self.cleaned_data.get("website") or "").strip()
        if value:
            # Bot detectado
            raise forms.ValidationError("Bot detected.")
        return value