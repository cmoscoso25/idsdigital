"""
Regenera creatividades existentes aplicando los nuevos estilos visuales.

Uso:
  python manage.py regenerar_creatividades            # todas
  python manage.py regenerar_creatividades --empresa 3  # solo empresa id=3
  python manage.py regenerar_creatividades --tipo post  # solo posts
"""

from django.core.management.base import BaseCommand
from nexa.models import CreatividadInstagram
from nexa.services.agentes.agente_diseno_instagram import generar_creatividad


class Command(BaseCommand):
    help = "Regenera creatividades existentes con los nuevos estilos del Director Creativo"

    def add_arguments(self, parser):
        parser.add_argument(
            "--empresa", type=int, default=None,
            help="ID de la empresa (EmpresaNexa) para filtrar",
        )
        parser.add_argument(
            "--tipo", type=str, default=None,
            choices=["post", "historia", "carrusel", "reel"],
            help="Tipo de creatividad a regenerar",
        )

    def handle(self, *args, **options):
        qs = CreatividadInstagram.objects.select_related(
            "contenido__empresa__memoria_marca",
        ).order_by("contenido__empresa", "tipo", "fecha_creacion")

        if options["empresa"]:
            qs = qs.filter(contenido__empresa_id=options["empresa"])
        if options["tipo"]:
            qs = qs.filter(tipo=options["tipo"])

        total = qs.count()
        if not total:
            self.stdout.write(self.style.WARNING("No se encontraron creatividades con esos filtros."))
            return

        self.stdout.write(f"Regenerando {total} creatividad(es)...\n")
        ok = errores = 0

        for i, cr in enumerate(qs, 1):
            try:
                empresa = cr.contenido.empresa
                memoria = getattr(empresa, "memoria_marca", None)
                r = generar_creatividad(empresa=empresa, memoria_marca=memoria, contenido=cr.contenido)

                cr.prompt_visual          = r["prompt_visual"]
                cr.estructura_visual_json = r["estructura_visual_json"]
                cr.render_html            = r.get("render_html", "")
                cr.render_css             = r.get("render_css", "")
                cr.estado                 = "generada"
                cr.estilo                 = r.get("estilo", "")
                cr.estilo_nombre          = r.get("estilo_nombre", "")
                cr.categoria_visual       = r.get("categoria_visual", "")
                cr.save(update_fields=[
                    "prompt_visual", "estructura_visual_json",
                    "render_html", "render_css", "estado",
                    "estilo", "estilo_nombre", "categoria_visual", "fecha_actualizacion",
                ])

                estilo_tag = f" [{cr.estilo_nombre}]" if cr.estilo_nombre else ""
                safe = str(cr).encode("ascii", errors="replace").decode()
                self.stdout.write(f"  [{i}/{total}] OK  {safe}{estilo_tag}")
                ok += 1

            except Exception as exc:
                safe = str(cr).encode("ascii", errors="replace").decode()
                self.stderr.write(f"  [{i}/{total}] ERR {safe} -- {exc}")
                errores += 1

        self.stdout.write("")
        if ok:
            self.stdout.write(self.style.SUCCESS(f"COMPLETADO: {ok} creatividad(es) regenerada(s) correctamente."))
        if errores:
            self.stdout.write(self.style.ERROR(f"ERRORES: {errores}. Revisa el output anterior."))
