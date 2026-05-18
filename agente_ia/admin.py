from django.contrib import admin, messages

from .models import (
    CategoriaConocimiento,
    RespuestaConocimiento,
    PreguntaAprendida,
    ConversacionAgente,
    MensajeAgente,
)


@admin.register(CategoriaConocimiento)
class CategoriaConocimientoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "activo",
        "fecha_creacion",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    list_filter = (
        "activo",
    )


@admin.register(RespuestaConocimiento)
class RespuestaConocimientoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "prioridad",
        "veces_utilizada",
        "activa",
    )

    search_fields = (
        "titulo",
        "palabras_clave",
        "respuesta",
    )

    list_filter = (
        "categoria",
        "activa",
    )

    list_editable = (
        "prioridad",
        "activa",
    )


@admin.action(description="Convertir preguntas seleccionadas en Respuestas IA")
def convertir_preguntas_en_respuestas(modeladmin, request, queryset):
    categoria_default = CategoriaConocimiento.objects.filter(
        nombre__icontains="Software"
    ).first()

    creadas = 0
    omitidas = 0

    for pregunta in queryset:
        if not pregunta.respuesta_sugerida.strip():
            omitidas += 1
            continue

        titulo = pregunta.pregunta[:120]

        ya_existe = RespuestaConocimiento.objects.filter(
            titulo=titulo
        ).exists()

        if ya_existe:
            omitidas += 1
            continue

        RespuestaConocimiento.objects.create(
            categoria=categoria_default,
            titulo=titulo,
            palabras_clave=pregunta.pregunta,
            respuesta=pregunta.respuesta_sugerida,
            prioridad=5,
            activa=True,
        )

        pregunta.respondida = True
        pregunta.save(
            update_fields=[
                "respondida",
                "ultima_vez",
            ]
        )

        creadas += 1

    if creadas:
        messages.success(
            request,
            f"{creadas} pregunta(s) fueron convertidas en Respuestas IA.",
        )

    if omitidas:
        messages.warning(
            request,
            f"{omitidas} pregunta(s) fueron omitidas porque no tenían respuesta sugerida o ya existían.",
        )


@admin.register(PreguntaAprendida)
class PreguntaAprendidaAdmin(admin.ModelAdmin):
    list_display = (
        "pregunta",
        "respondida",
        "veces_preguntada",
        "ultima_vez",
    )

    search_fields = (
        "pregunta",
        "respuesta_sugerida",
    )

    list_filter = (
        "respondida",
    )

    list_editable = (
        "respondida",
    )

    actions = [
        convertir_preguntas_en_respuestas,
    ]

    fieldsets = (
        (
            "Pregunta detectada por el agente",
            {
                "fields": (
                    "pregunta",
                    "veces_preguntada",
                    "respondida",
                )
            },
        ),
        (
            "Aprendizaje del agente",
            {
                "fields": (
                    "respuesta_sugerida",
                ),
                "description": (
                    "Escribe aquí la respuesta que el agente deberá usar en futuras consultas similares. "
                    "Luego marca la pregunta como respondida o usa la acción para convertirla en Respuesta IA."
                ),
            },
        ),
    )

    readonly_fields = (
        "veces_preguntada",
    )


class MensajeInline(admin.TabularInline):
    model = MensajeAgente

    extra = 0

    readonly_fields = (
        "rol",
        "mensaje",
        "fecha_creacion",
    )

    can_delete = False


@admin.register(ConversacionAgente)
class ConversacionAgenteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "empresa",
        "correo",
        "telefono",
        "fecha_creacion",
    )

    search_fields = (
        "nombre",
        "empresa",
        "correo",
        "telefono",
    )

    readonly_fields = (
        "fecha_creacion",
    )

    inlines = [
        MensajeInline,
    ]


@admin.register(MensajeAgente)
class MensajeAgenteAdmin(admin.ModelAdmin):
    list_display = (
        "conversacion",
        "rol",
        "mensaje",
        "fecha_creacion",
    )

    search_fields = (
        "mensaje",
    )

    list_filter = (
        "rol",
        "fecha_creacion",
    )

    readonly_fields = (
        "conversacion",
        "rol",
        "mensaje",
        "fecha_creacion",
    )