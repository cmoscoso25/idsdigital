from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nexa", "0010_add_imagen_generada_to_creatividad"),
    ]

    operations = [
        migrations.CreateModel(
            name="EstiloVisualInstagram",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(help_text="ID único del estilo, ej: corporate_kpi", max_length=50, unique=True)),
                ("nombre", models.CharField(help_text="Nombre legible para mostrar en UI", max_length=100)),
                ("descripcion", models.TextField(blank=True, help_text="Descripción breve del look & feel del estilo")),
                ("categoria", models.CharField(
                    choices=[
                        ("corporativo", "Corporativo"),
                        ("tech", "Tecnología / IA"),
                        ("editorial", "Editorial"),
                        ("educativo", "Educativo"),
                        ("narrativo", "Narrativo / Storytelling"),
                    ],
                    default="corporativo",
                    max_length=30,
                )),
                ("activo", models.BooleanField(default=True, help_text="Si está desactivado no se usa en la selección")),
            ],
            options={
                "verbose_name": "Estilo Visual Instagram",
                "verbose_name_plural": "Estilos Visuales Instagram",
                "ordering": ["categoria", "nombre"],
            },
        ),
        migrations.AddIndex(
            model_name="estilovisualinstagram",
            index=models.Index(fields=["activo", "categoria"], name="nexa_estilo_activo_cat_idx"),
        ),
    ]
