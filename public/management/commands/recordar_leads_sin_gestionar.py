from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from public.models import DemoRequest
from public.services.email_service import enviar_notificacion_interna


class Command(BaseCommand):
    help = "Revisa solicitudes sin gestionar hace más de 48hrs y envía recordatorio"

    def handle(self, *args, **options):
        # Calculamos el límite de tiempo: hace 48 horas
        limite = timezone.now() - timedelta(hours=48)

        # Buscamos solicitudes nuevas que llevan más de 48hrs sin gestionar
        solicitudes_sin_gestionar = DemoRequest.objects.filter(
            status=DemoRequest.Status.NEW,
            created_at__lte=limite,
            converted_to_lead=False,
        )

        total = solicitudes_sin_gestionar.count()

        if total == 0:
            self.stdout.write("No hay solicitudes sin gestionar. Todo al día.")
            return

        # Enviamos un recordatorio por cada solicitud sin gestionar
        for solicitud in solicitudes_sin_gestionar:
            horas_esperando = int((timezone.now() - solicitud.created_at).total_seconds() / 3600)

            try:
                import resend
                from django.conf import settings

                resend.Emails.send({
                    "from": "CRM IDS <hola@idsdigital.cl>",
                    "to": ["contacto@idsdigital.cl"],
                    "subject": f"⚠️ Solicitud sin gestionar hace {horas_esperando}hrs — {solicitud.company or solicitud.name}",
                    "html": f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">

                        <div style="background: #0f172a; padding: 24px 32px; border-radius: 10px 10px 0 0;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 18px; font-weight: 700;">
                                ⚠️ Solicitud sin gestionar
                            </h1>
                            <p style="color: #94a3b8; margin: 4px 0 0; font-size: 13px;">CRM · IDS Digital</p>
                        </div>

                        <div style="background: #f8fafc; padding: 32px; border: 1px solid #e2e8f0;
                                    border-top: none; border-radius: 0 0 10px 10px;">

                            <p style="color: #dc2626; font-weight: 600; font-size: 15px; margin-bottom: 20px;">
                                Esta solicitud lleva <strong>{horas_esperando} horas</strong> esperando respuesta.
                            </p>

                            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                                <tr>
                                    <td style="padding: 10px 12px; color: #64748b; width: 30%;
                                               background: #f1f5f9; border-radius: 4px; font-weight: 600;">
                                        Nombre
                                    </td>
                                    <td style="padding: 10px 12px; background: #ffffff;">
                                        {solicitud.name}
                                    </td>
                                </tr>
                                <tr style="height: 4px;"></tr>
                                <tr>
                                    <td style="padding: 10px 12px; color: #64748b;
                                               background: #f1f5f9; border-radius: 4px; font-weight: 600;">
                                        Email
                                    </td>
                                    <td style="padding: 10px 12px; background: #ffffff;">
                                        <a href="mailto:{solicitud.email}" style="color: #3b82f6;">
                                            {solicitud.email}
                                        </a>
                                    </td>
                                </tr>
                                <tr style="height: 4px;"></tr>
                                <tr>
                                    <td style="padding: 10px 12px; color: #64748b;
                                               background: #f1f5f9; border-radius: 4px; font-weight: 600;">
                                        Empresa
                                    </td>
                                    <td style="padding: 10px 12px; background: #ffffff;">
                                        {solicitud.company or '—'}
                                    </td>
                                </tr>
                                <tr style="height: 4px;"></tr>
                                <tr>
                                    <td style="padding: 10px 12px; color: #64748b;
                                               background: #f1f5f9; border-radius: 4px; font-weight: 600;">
                                        Asunto
                                    </td>
                                    <td style="padding: 10px 12px; background: #ffffff;">
                                        {solicitud.subject or '—'}
                                    </td>
                                </tr>
                                <tr style="height: 4px;"></tr>
                                <tr>
                                    <td style="padding: 10px 12px; color: #64748b;
                                               background: #f1f5f9; border-radius: 4px; font-weight: 600;">
                                        Recibida
                                    </td>
                                    <td style="padding: 10px 12px; background: #ffffff;">
                                        {solicitud.created_at.strftime('%d-%m-%Y %H:%M')}
                                    </td>
                                </tr>
                            </table>

                            <div style="text-align: center; margin-top: 28px;">
                                <a href="https://idsdigital.cl/panel/solicitudes/"
                                   style="background: #dc2626; color: #ffffff; text-decoration: none;
                                          padding: 14px 32px; border-radius: 8px; font-weight: 600;
                                          font-size: 15px; display: inline-block;">
                                    Gestionar ahora →
                                </a>
                            </div>

                            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 28px 0 16px;">

                            <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                                Este recordatorio fue generado automáticamente por el CRM de IDS Digital.
                            </p>
                        </div>

                    </div>
                    """,
                })

                self.stdout.write(
                    f"Recordatorio enviado: {solicitud.name} ({solicitud.email}) — {horas_esperando}hrs esperando"
                )

            except Exception as e:
                self.stdout.write(f"Error al enviar recordatorio para {solicitud.email}: {e}")

        self.stdout.write(f"Total recordatorios enviados: {total}")