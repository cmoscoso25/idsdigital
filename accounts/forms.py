from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Workspace, Membership

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "usuario"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••••"}),
    )

class WorkspaceSelectForm(forms.Form):
    workspace_id = forms.ChoiceField(label="Selecciona empresa", widget=forms.Select(attrs={"class": "input"}))

    def __init__(self, *args, memberships=None, **kwargs):
        super().__init__(*args, **kwargs)
        memberships = memberships or []
        self.fields["workspace_id"].choices = [
            (m.workspace_id, f"{m.workspace.name} ({m.get_role_display()})") for m in memberships
        ]