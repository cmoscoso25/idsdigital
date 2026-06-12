from django.core.management.base import BaseCommand
from billing.models import Plan


PLANES = [
    {
        "tier": Plan.STARTER,
        "nombre": "Starter",
        "precio_usd": "15.00",
        "posts_por_mes": 20,
        "orden": 1,
    },
    {
        "tier": Plan.PRO,
        "nombre": "Pro",
        "precio_usd": "29.00",
        "posts_por_mes": 40,
        "orden": 2,
    },
    {
        "tier": Plan.AGENCY,
        "nombre": "Agency",
        "precio_usd": "79.00",
        "posts_por_mes": 120,
        "orden": 3,
    },
]


class Command(BaseCommand):
    help = "Crea los planes de Nexa AI si no existen"

    def handle(self, *args, **options):
        for datos in PLANES:
            plan, created = Plan.objects.get_or_create(
                tier=datos["tier"],
                defaults=datos,
            )
            estado = "creado" if created else "ya existe"
            self.stdout.write(f"  {plan.nombre} — {estado}")
        self.stdout.write(self.style.SUCCESS("seed_planes completado"))
