from django.utils.deprecation import MiddlewareMixin
from .models import Membership

class CurrentWorkspaceMiddleware(MiddlewareMixin):
    """
    Inyecta request.workspace y request.membership
    basado en session['current_workspace_id'].
    Si no existe, toma el primero disponible.
    """

    def process_request(self, request):
        request.workspace = None
        request.membership = None

        if not request.user.is_authenticated:
            return

        memberships = (
            Membership.objects
            .select_related("workspace")
            .filter(user=request.user, is_active=True)
            .order_by("workspace__name")
        )
        if not memberships.exists():
            return

        current_id = request.session.get("current_workspace_id")
        membership = None

        if current_id:
            membership = memberships.filter(workspace_id=current_id).first()

        if membership is None:
            membership = memberships.first()
            request.session["current_workspace_id"] = membership.workspace_id

        request.membership = membership
        request.workspace = membership.workspace