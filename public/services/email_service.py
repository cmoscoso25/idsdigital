import resend
from django.conf import settings


def enviar_bienvenida_solicitud(name: str, email: str, subject: str = "") -> bool:
    """
    Le manda un email de bienvenida al lead apenas envía el formulario.
    Le confirma que recibimos su solicitud y qué esperar.
    """
    asunto_texto = f" sobre <strong>{subject}</strong>" if subject else ""

    try:
        resend.Emails.send({
            "from": "IDS Digital <hola@idsdigital.cl>",
            "to": [email],
            "subject": "Recibimos tu solicitud – IDS Digital",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">

                <div style="background: #0f172a; padding: 28px 32px; border-radius: 10px 10px 0 0;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 700;">IDS Digital</h1>
                    <p style="color: #94a3b8; margin: 4px 0 0; font-size: 13px;">
                        Consultora tecnológica · Software · IA · Automatización
                    </p>
                </div>

                <div style="background: #f8fafc; padding: 36px 32px; border: 1px solid #e2e8f0;
                            border-top: none; border-radius: 0 0 10px 10px;">

                    <h2 style="margin-top: 0; font-size: 20px; color: #1e293b;">
                        Hola {name}, recibimos tu mensaje 👋
                    </h2>

                    <p style="color: #475569; line-height: 1.7;">
                        Gracias por contactarnos{asunto_texto}.
                        Nuestro equipo revisará tu solicitud y te responderá a la brevedad
                        con un enfoque claro y alineado a tu necesidad.
                    </p>

                    <div style="background: #ffffff; border-left: 4px solid #3b82f6; padding: 20px 24px;
                                margin: 28px 0; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                        <p style="margin: 0 0 10px; font-weight: 700; color: #1e293b;">¿Qué sigue?</p>
                        <ul style="color: #475569; margin: 0; padding-left: 20px; line-height: 2;">
                            <li>Revisamos tu solicitud en detalle</li>
                            <li>Te contactamos para coordinar un diagnóstico</li>
                            <li>Te proponemos una solución a medida y sin compromiso</li>
                        </ul>
                    </div>

                    <p style="color: #475569; line-height: 1.7;">
                        Si tienes alguna urgencia, puedes escribirnos directamente a
                        <a href="mailto:contacto@idsdigital.cl" style="color: #3b82f6; text-decoration: none;">
                            contacto@idsdigital.cl
                        </a>
                    </p>

                    <div style="text-align: center; margin: 32px 0 16px;">
                        <a href="https://www.idsdigital.cl"
                           style="background: #3b82f6; color: #ffffff; text-decoration: none;
                                  padding: 14px 32px; border-radius: 8px; font-weight: 600;
                                  font-size: 15px; display: inline-block;">
                            Visitar IDS Digital →
                        </a>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 28px 0 16px;">

                    <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                        IDS Digital · Inteligencia Digital y Sistemas · Santiago, Chile
                    </p>
                </div>

            </div>
            """,
        })
        return True

    except Exception as e:
        print(f"[IDS Email] Error al enviar bienvenida a {email}: {e}")
        return False


def enviar_notificacion_interna(name: str, email: str, company: str = "", subject: str = "", message: str = "") -> bool:
    """
    Nos avisa internamente cuando llega una solicitud nueva.
    Incluye los datos del lead y un link directo al CRM.
    """
    empresa_texto = company if company else "No indicó"
    asunto_texto = subject if subject else "No indicó"
    mensaje_texto = message if message else "Sin mensaje"

    try:
        resend.Emails.send({
            "from": "CRM IDS <hola@idsdigital.cl>",
            "to": ["contacto@idsdigital.cl", "cmoscosom@gmail.com"],
            "subject": f"🔔 Nueva solicitud de {company or name}",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">

                <div style="background: #0f172a; padding: 24px 32px; border-radius: 10px 10px 0 0;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 18px; font-weight: 700;">
                        🔔 Nueva solicitud entrante
                    </h1>
                    <p style="color: #94a3b8; margin: 4px 0 0; font-size: 13px;">CRM · IDS Digital</p>
                </div>

                <div style="background: #f8fafc; padding: 32px; border: 1px solid #e2e8f0;
                            border-top: none; border-radius: 0 0 10px 10px;">

                    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                        <tr>
                            <td style="padding: 10px 12px; color: #64748b; width: 30%; background: #f1f5f9;
                                       border-radius: 4px; font-weight: 600;">Nombre</td>
                            <td style="padding: 10px 12px; background: #ffffff;">{name}</td>
                        </tr>
                        <tr style="height: 4px;"></tr>
                        <tr>
                            <td style="padding: 10px 12px; color: #64748b; background: #f1f5f9;
                                       border-radius: 4px; font-weight: 600;">Email</td>
                            <td style="padding: 10px 12px; background: #ffffff;">
                                <a href="mailto:{email}" style="color: #3b82f6; text-decoration: none;">{email}</a>
                            </td>
                        </tr>
                        <tr style="height: 4px;"></tr>
                        <tr>
                            <td style="padding: 10px 12px; color: #64748b; background: #f1f5f9;
                                       border-radius: 4px; font-weight: 600;">Empresa</td>
                            <td style="padding: 10px 12px; background: #ffffff;">{empresa_texto}</td>
                        </tr>
                        <tr style="height: 4px;"></tr>
                        <tr>
                            <td style="padding: 10px 12px; color: #64748b; background: #f1f5f9;
                                       border-radius: 4px; font-weight: 600;">Asunto</td>
                            <td style="padding: 10px 12px; background: #ffffff;">{asunto_texto}</td>
                        </tr>
                        <tr style="height: 4px;"></tr>
                        <tr>
                            <td style="padding: 10px 12px; color: #64748b; background: #f1f5f9;
                                       border-radius: 4px; font-weight: 600; vertical-align: top;">Mensaje</td>
                            <td style="padding: 10px 12px; background: #ffffff; line-height: 1.6;
                                       color: #475569;">{mensaje_texto}</td>
                        </tr>
                    </table>

                    <div style="text-align: center; margin-top: 28px;">
                        <a href="https://idsdigital.cl/panel/solicitudes/"
                           style="background: #3b82f6; color: #ffffff; text-decoration: none;
                                  padding: 14px 32px; border-radius: 8px; font-weight: 600;
                                  font-size: 15px; display: inline-block;">
                            Ver en el CRM →
                        </a>
                    </div>

                    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 28px 0 16px;">

                    <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                        Este mensaje fue generado automáticamente por el CRM de IDS Digital.
                    </p>
                </div>

            </div>
            """,
        })
        return True

    except Exception as e:
        print(f"[IDS Email] Error al enviar notificación interna: {e}")
        return False