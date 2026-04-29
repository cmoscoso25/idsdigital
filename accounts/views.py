from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, WorkspaceSelectForm
from .models import Membership


class AccountsLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        memberships = Membership.objects.filter(user=user, is_active=True).select_related("workspace")

        if not memberships.exists():
            messages.error(self.request, "Tu usuario no tiene acceso a ninguna empresa (workspace).")
            return redirect("accounts:login")

        # Si tiene 1 sola empresa, entra directo al CRM
        if memberships.count() == 1:
            self.request.session["current_workspace_id"] = memberships.first().workspace_id
            return redirect("crm:lead_list")  # ✅ CORREGIDO

        # Si tiene varias, mandamos selector
        return redirect("accounts:workspace_select")


class AccountsLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@login_required
def workspace_select(request):
    memberships = (
        Membership.objects
        .filter(user=request.user, is_active=True)
        .select_related("workspace")
        .order_by("workspace__name")
    )

    if memberships.count() <= 1:
        if memberships.exists():
            request.session["current_workspace_id"] = memberships.first().workspace_id
        return redirect("crm:lead_list")  # ✅ CORREGIDO

    if request.method == "POST":
        form = WorkspaceSelectForm(request.POST, memberships=memberships)
        if form.is_valid():
            request.session["current_workspace_id"] = int(form.cleaned_data["workspace_id"])
            return redirect("crm:lead_list")  # ✅ CORREGIDO
    else:
        form = WorkspaceSelectForm(memberships=memberships)

    return render(request, "accounts/workspace_select.html", {
        "form": form,
        "memberships": memberships
    })