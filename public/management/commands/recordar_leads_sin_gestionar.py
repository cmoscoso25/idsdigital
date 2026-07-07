from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from public.models import DemoRequest


class Command(BaseCommand):
    help = (
        "Revisa solicitudes sin gestionar hace más de 48hrs. "
        "El envío de correo recordatorio está deshabilitado: al no marcar la solicitud "
        "como notificada, reenviaba un correo cada vez que el cron corría, generando spam."
    )

    def handle(self, *args, **options):
        limite = timezone.now() - timedelta(hours=48)

        solicitudes_sin_gestionar = DemoRequest.objects.filter(
            status=DemoRequest.Status.NEW,
            created_at__lte=limite,
            converted_to_lead=False,
        )

        total = solicitudes_sin_gestionar.count()

        if total == 0:
            self.stdout.write("No hay solicitudes sin gestionar. Todo al día.")
            return

        for solicitud in solicitudes_sin_gestionar:
            horas_esperando = int((timezone.now() - solicitud.created_at).total_seconds() / 3600)
            self.stdout.write(
                f"Sin gestionar: {solicitud.name} ({solicitud.email}) — {horas_esperando}hrs esperando"
            )

        self.stdout.write(f"Total sin gestionar: {total} (envío de correo deshabilitado)")
