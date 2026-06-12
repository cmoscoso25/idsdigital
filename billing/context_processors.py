from django.utils import timezone

from billing.models import Subscription


def subscription(request):
    if not request.user.is_authenticated:
        return {}
    sub, _ = Subscription.objects.get_or_create(
        usuario=request.user,
        defaults={
            "estado": Subscription.TRIAL,
            "trial_fin": timezone.now() + timezone.timedelta(days=14),
        },
    )
    return {"subscription": sub}
