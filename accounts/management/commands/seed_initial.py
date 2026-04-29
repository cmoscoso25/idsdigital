from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from accounts.models import Workspace, Membership  # ajusta si tus nombres difieren


User = get_user_model()


class Command(BaseCommand):
    help = "Crea workspace inicial + usuario admin + membership (seed dev)."

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, default="admin@ids.cl")
        parser.add_argument("--password", type=str, default="Admin12345!")
        parser.add_argument("--workspace", type=str, default="Inteligencia Digital y Sistemas SpA")

    @transaction.atomic
    def handle(self, *args, **opts):
        email = opts["email"].strip().lower()
        password = opts["password"]
        ws_name = opts["workspace"].strip()

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password", "is_staff", "is_superuser"])
            self.stdout.write(self.style.SUCCESS(f"✅ Usuario creado: {email}"))
        else:
            self.stdout.write(self.style.WARNING(f"ℹ️ Usuario ya existía: {email}"))

        ws, ws_created = Workspace.objects.get_or_create(
            name=ws_name,
            defaults={"created_at": timezone.now()} if hasattr(Workspace, "created_at") else {},
        )

        if ws_created:
            self.stdout.write(self.style.SUCCESS(f"✅ Workspace creado: {ws_name}"))
        else:
            self.stdout.write(self.style.WARNING(f"ℹ️ Workspace ya existía: {ws_name}"))

        # Membership (ajusta campos según tu modelo)
        mem, mem_created = Membership.objects.get_or_create(
            workspace=ws,
            user=user,
            defaults={"role": "admin"},
        )

        if mem_created:
            self.stdout.write(self.style.SUCCESS("✅ Membership admin creada"))
        else:
            self.stdout.write(self.style.WARNING("ℹ️ Membership ya existía"))

        self.stdout.write(self.style.SUCCESS("🚀 Seed finalizado"))