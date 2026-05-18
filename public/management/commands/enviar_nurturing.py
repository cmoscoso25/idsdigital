from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import resend


class Command(BaseCommand):
    help = "Envía emails de nurturing automático a leads según los días transcurridos"

    def handle(self, *args, **options):
        from public.models import DemoRequest

        ahora = timezone.now()
        enviados = 0

        # Buscamos solicitudes que no fueron convertidas ni descartadas
        solicitudes = DemoRequest.objects.filter(
            converted_to_lead=False,
            status__in=["new", "in_review", "contacted"],
        )

        for solicitud in solicitudes:
            dias = (ahora - solicitud.created_at).days

            # DÍA 3 — Seguimiento inicial
            if dias >= 3 and not solicitud.nurturing_dia3_enviado:
                exito = self._enviar_dia3(solicitud)
                if exito:
                    solicitud.nurturing_dia3_enviado = True
                    solicitud.save(update_fields=["nurturing_dia3_enviado", "updated_at"])
                    enviados += 1
                    self.stdout.write(f"[Día 3] Enviado a {solicitud.email}")

            # DÍA 7 — Contenido de valor
            elif dias >= 7 and not solicitud.nurturing_dia7_enviado:
                exito = self._enviar_dia7(solicitud)
                if exito:
                    solicitud.nurturing_dia7_enviado = True
                    solicitud.save(update_fields=["nurturing_dia7_enviado", "updated_at"])
                    enviados += 1
                    self.stdout.write(f"[Día 7] Enviado a {solicitud.email}")

            # DÍA 14 — Último intento
            elif dias >= 14 and not solicitud.nurturing_dia14_enviado:
                exito = self._enviar_dia14(solicitud)
                if exito:
                    solicitud.nurturing_dia14_enviado = True
                    solicitud.save(update_fields=["nurturing_dia14_enviado", "updated_at"])
                    enviados += 1
                    self.stdout.write(f"[Día 14] Enviado a {solicitud.email}")

        self.stdout.write(f"Nurturing completado. Total enviados: {enviados}")

    def _enviar_dia3(self, solicitud) -> bool:
        """
        Día 3 — Seguimiento suave, recordamos que estamos disponibles.
        """
        nombre = solicitud.name.split()[0] if solicitud.name else "hola"
        asunto_texto = f" sobre {solicitud.subject}" if solicitud.subject else ""

        try:
            resend.Emails.send({
                "from": "IDS Digital <hola@idsdigital.cl>",
                "to": [solicitud.email],
                "subject": f"{nombre}, ¿pudiste revisar nuestra propuesta?",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">
                    <div style="background: #0f172a; padding: 24px 32px; border-radius: 10px 10px 0 0;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <svg width="28" height="28" viewBox="0 0 60 60" fill="none">
                                <circle cx="30" cy="28" r="7" fill="#3b82f6"/>
                                <circle cx="14" cy="14" r="4.5" fill="#60a5fa"/>
                                <circle cx="46" cy="14" r="4.5" fill="#60a5fa"/>
                                <line x1="30" y1="21" x2="16" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                                <line x1="30" y1="21" x2="44" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                            </svg>
                            <span style="color: #ffffff; font-size: 16px; font-weight: 600;">IDS Digital</span>
                        </div>
                    </div>
                    <div style="background: #f8fafc; padding: 32px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px;">
                        <h2 style="color: #0f172a; margin-top: 0; font-size: 18px;">
                            Hola {nombre}, ¿pudiste revisar nuestra propuesta?
                        </h2>
                        <p style="color: #475569; line-height: 1.7;">
                            Hace unos días nos contactaste{asunto_texto}. Queremos asegurarnos de que hayas recibido bien nuestro mensaje y que no haya quedado en el limbo.
                        </p>
                        <p style="color: #475569; line-height: 1.7;">
                            Si tienes preguntas, si necesitas más información o si quieres agendar una llamada para conversar tu caso, estamos disponibles. Sin presión, sin compromiso.
                        </p>
                        <div style="text-align: center; margin: 28px 0;">
                            <a href="https://www.idsdigital.cl/#contacto"
                               style="background: #2563eb; color: #ffffff; text-decoration: none;
                                      padding: 13px 28px; border-radius: 7px; font-size: 14px;
                                      font-weight: 600; display: inline-block;">
                                Conversar con IDS Digital →
                            </a>
                        </div>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">
                        <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                            IDS Digital · Inteligencia Digital y Sistemas · Santiago, Chile
                        </p>
                    </div>
                </div>
                """,
            })
            return True
        except Exception as e:
            self.stdout.write(f"Error día 3 para {solicitud.email}: {e}")
            return False

    def _enviar_dia7(self, solicitud) -> bool:
        """
        Día 7 — Entregamos contenido de valor relacionado a su necesidad.
        """
        nombre = solicitud.name.split()[0] if solicitud.name else "hola"
        subject = (solicitud.subject or "").lower()

        # Elegimos el artículo según lo que seleccionó en el formulario
        if "automatización" in subject or "automatizacion" in subject:
            articulo_titulo = "Por qué las empresas chilenas siguen usando Excel y cómo automatizar sus procesos"
            articulo_url = "https://www.idsdigital.cl/blog/por-que-las-empresas-chilenas-siguen-usando-excel-y-como-automatizar-sus-procesos-en-2026/"
            articulo_desc = "Un análisis práctico de cómo las empresas en Chile pueden dejar de perder horas en tareas manuales y dar el primer paso hacia la automatización."
        elif "software" in subject:
            articulo_titulo = "Cuánto cuesta desarrollar software a medida en Chile y qué debe incluir"
            articulo_url = "https://www.idsdigital.cl/blog/cuanto-cuesta-desarrollar-software-a-medida-en-chile-y-que-debe-incluir/"
            articulo_desc = "Una guía clara sobre qué factores determinan el precio del software a medida y qué deberías exigir antes de contratar."
        elif "digitaliz" in subject:
            articulo_titulo = "Cómo digitalizar una empresa en Chile sin gastar una fortuna"
            articulo_url = "https://www.idsdigital.cl/blog/como-digitalizar-una-empresa-en-chile-sin-gastar-una-fortuna-guia-practica-2026/"
            articulo_desc = "Una guía práctica para digitalizar tu empresa paso a paso, con foco en resultados reales y sin desperdiciar recursos."
        else:
            articulo_titulo = "Automatización de procesos para pymes en Chile: casos reales y por dónde empezar"
            articulo_url = "https://www.idsdigital.cl/blog/automatizacion-de-procesos-para-pymes-en-chile-casos-reales-y-por-donde-empezar/"
            articulo_desc = "Casos reales de empresas chilenas que redujeron trabajo manual y mejoraron su eficiencia operativa sin grandes inversiones."

        try:
            resend.Emails.send({
                "from": "IDS Digital <hola@idsdigital.cl>",
                "to": [solicitud.email],
                "subject": f"Algo que podría ayudarte, {nombre}",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">
                    <div style="background: #0f172a; padding: 24px 32px; border-radius: 10px 10px 0 0;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <svg width="28" height="28" viewBox="0 0 60 60" fill="none">
                                <circle cx="30" cy="28" r="7" fill="#3b82f6"/>
                                <circle cx="14" cy="14" r="4.5" fill="#60a5fa"/>
                                <circle cx="46" cy="14" r="4.5" fill="#60a5fa"/>
                                <line x1="30" y1="21" x2="16" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                                <line x1="30" y1="21" x2="44" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                            </svg>
                            <span style="color: #ffffff; font-size: 16px; font-weight: 600;">IDS Digital</span>
                        </div>
                    </div>
                    <div style="background: #f8fafc; padding: 32px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px;">
                        <h2 style="color: #0f172a; margin-top: 0; font-size: 18px;">
                            Hola {nombre}, algo que podría ayudarte
                        </h2>
                        <p style="color: #475569; line-height: 1.7;">
                            Mientras revisamos tu solicitud, preparamos un artículo que creemos puede ser útil para tu caso:
                        </p>
                        <div style="background: #ffffff; border-left: 4px solid #2563eb; padding: 20px 24px;
                                    margin: 20px 0; border-radius: 6px; border: 0.5px solid #e2e8f0;">
                            <div style="font-size: 13px; font-weight: 600; color: #2563eb; margin-bottom: 6px;">
                                Artículo recomendado
                            </div>
                            <div style="font-size: 15px; font-weight: 600; color: #0f172a; margin-bottom: 8px;">
                                {articulo_titulo}
                            </div>
                            <p style="color: #64748b; font-size: 13px; line-height: 1.6; margin: 0 0 14px;">
                                {articulo_desc}
                            </p>
                            <a href="{articulo_url}"
                               style="color: #2563eb; font-size: 13px; font-weight: 600; text-decoration: none;">
                                Leer artículo →
                            </a>
                        </div>
                        <p style="color: #475569; line-height: 1.7;">
                            Si quieres conversar tu caso directamente, seguimos disponibles para ayudarte.
                        </p>
                        <div style="text-align: center; margin: 28px 0;">
                            <a href="https://www.idsdigital.cl/#contacto"
                               style="background: #2563eb; color: #ffffff; text-decoration: none;
                                      padding: 13px 28px; border-radius: 7px; font-size: 14px;
                                      font-weight: 600; display: inline-block;">
                                Solicitar diagnóstico gratuito →
                            </a>
                        </div>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">
                        <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                            IDS Digital · Inteligencia Digital y Sistemas · Santiago, Chile
                        </p>
                    </div>
                </div>
                """,
            })
            return True
        except Exception as e:
            self.stdout.write(f"Error día 7 para {solicitud.email}: {e}")
            return False

    def _enviar_dia14(self, solicitud) -> bool:
        """
        Día 14 — Último intento, cierre amable.
        """
        nombre = solicitud.name.split()[0] if solicitud.name else "hola"

        try:
            resend.Emails.send({
                "from": "IDS Digital <hola@idsdigital.cl>",
                "to": [solicitud.email],
                "subject": f"{nombre}, ¿aún tienes esa necesidad tecnológica?",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">
                    <div style="background: #0f172a; padding: 24px 32px; border-radius: 10px 10px 0 0;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <svg width="28" height="28" viewBox="0 0 60 60" fill="none">
                                <circle cx="30" cy="28" r="7" fill="#3b82f6"/>
                                <circle cx="14" cy="14" r="4.5" fill="#60a5fa"/>
                                <circle cx="46" cy="14" r="4.5" fill="#60a5fa"/>
                                <line x1="30" y1="21" x2="16" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                                <line x1="30" y1="21" x2="44" y2="16" stroke="#3b82f6" stroke-width="1.5"/>
                            </svg>
                            <span style="color: #ffffff; font-size: 16px; font-weight: 600;">IDS Digital</span>
                        </div>
                    </div>
                    <div style="background: #f8fafc; padding: 32px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px;">
                        <h2 style="color: #0f172a; margin-top: 0; font-size: 18px;">
                            {nombre}, ¿aún tienes esa necesidad tecnológica?
                        </h2>
                        <p style="color: #475569; line-height: 1.7;">
                            Hace un par de semanas nos contactaste y queremos asegurarnos de que hayas encontrado lo que necesitabas. Si aún tienes esa necesidad, seguimos aquí.
                        </p>
                        <p style="color: #475569; line-height: 1.7;">
                            Muchas veces los proyectos se posponen por falta de tiempo o porque no es el momento. Si ese es tu caso, no hay problema. Cuando estés listo, estaremos disponibles.
                        </p>
                        <div style="background: #eff6ff; border-radius: 8px; padding: 20px 24px; margin: 20px 0;">
                            <p style="color: #1e40af; font-size: 14px; font-weight: 600; margin: 0 0 8px;">
                                Lo que ofrecemos sigue igual:
                            </p>
                            <ul style="color: #1e40af; font-size: 13px; margin: 0; padding-left: 18px; line-height: 2;">
                                <li>Diagnóstico gratuito y sin compromiso</li>
                                <li>Propuesta clara alineada a tu presupuesto</li>
                                <li>Solución a medida para tu operación</li>
                            </ul>
                        </div>
                        <div style="text-align: center; margin: 28px 0;">
                            <a href="https://www.idsdigital.cl/#contacto"
                               style="background: #2563eb; color: #ffffff; text-decoration: none;
                                      padding: 13px 28px; border-radius: 7px; font-size: 14px;
                                      font-weight: 600; display: inline-block;">
                                Retomar conversación →
                            </a>
                        </div>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">
                        <p style="color: #94a3b8; font-size: 12px; margin: 0; text-align: center;">
                            IDS Digital · Inteligencia Digital y Sistemas · Santiago, Chile<br>
                            Este es nuestro último seguimiento automático. No recibirás más emails de este tipo.
                        </p>
                    </div>
                </div>
                """,
            })
            return True
        except Exception as e:
            self.stdout.write(f"Error día 14 para {solicitud.email}: {e}")
            return False