from accounts.models import Membership

def role_of(request):
    if not getattr(request, "membership", None):
        return None
    return request.membership.role

def can_view_all_leads(request) -> bool:
    r = role_of(request)
    return r in {Membership.Role.ADMIN, Membership.Role.SUPERVISOR}

def can_edit_leads(request) -> bool:
    r = role_of(request)
    return r in {Membership.Role.ADMIN, Membership.Role.SUPERVISOR, Membership.Role.SALES}

def can_manage_users(request) -> bool:
    r = role_of(request)
    return r in {Membership.Role.ADMIN}