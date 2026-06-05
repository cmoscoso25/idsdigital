from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nexa", "0009_add_categoria_visual_to_creatividad"),
    ]

    operations = [
        migrations.AddField(
            model_name="creatividadinstagram",
            name="imagen_generada",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="nexa/creatividades/",
                help_text="Imagen real generada por IA (OpenAI DALL-E, Flux, Ideogram, Gemini). Si existe, reemplaza el mockup HTML.",
            ),
        ),
        migrations.AddField(
            model_name="creatividadinstagram",
            name="proveedor_ia",
            field=models.CharField(
                blank=True,
                default="",
                max_length=30,
                help_text="Proveedor usado para generar la imagen: openai, flux, ideogram, gemini",
            ),
        ),
        migrations.AddField(
            model_name="creatividadinstagram",
            name="fecha_generacion_imagen",
            field=models.DateTimeField(
                blank=True,
                null=True,
                help_text="Fecha y hora en que se generó la imagen IA",
            ),
        ),
    ]
