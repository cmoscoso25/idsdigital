from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nexa', '0008_add_fecha_actualizacion_to_creatividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatividadinstagram',
            name='categoria_visual',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Categoría temática detectada: software, ia, automatizacion, marketing, etc.',
                max_length=30,
            ),
        ),
    ]
