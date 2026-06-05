from django.contrib import admin
from .models import EmpresaNexa, MemoriaMarca, ContenidoGenerado, CreatividadInstagram, EstrategiaMensual


@admin.register(EmpresaNexa)
class EmpresaNexaAdmin(admin.ModelAdmin):
    list_display = ["nombre_empresa", "rubro", "tono_marca", "objetivo_principal", "usuario", "fecha_creacion"]
    list_filter = ["tono_marca", "objetivo_principal", "fecha_creacion"]
    search_fields = ["nombre_empresa", "rubro", "usuario__email", "usuario__username"]
    readonly_fields = ["fecha_creacion"]
    raw_id_fields = ["usuario"]


@admin.register(MemoriaMarca)
class MemoriaMarcaAdmin(admin.ModelAdmin):
    list_display = ["empresa", "propuesta_valor_corta"]
    search_fields = ["empresa__nombre_empresa", "palabras_clave", "propuesta_valor"]
    raw_id_fields = ["empresa"]

    @admin.display(description="Propuesta de valor")
    def propuesta_valor_corta(self, obj):
        return obj.propuesta_valor[:80]


@admin.register(ContenidoGenerado)
class ContenidoGeneradoAdmin(admin.ModelAdmin):
    list_display = ["titulo_corto", "empresa", "tipo_contenido", "estado", "fecha_creacion"]
    list_filter = ["tipo_contenido", "estado", "fecha_creacion"]
    search_fields = ["titulo", "empresa__nombre_empresa", "copy"]
    readonly_fields = ["fecha_creacion"]
    list_editable = ["estado"]
    raw_id_fields = ["empresa"]

    @admin.display(description="Título")
    def titulo_corto(self, obj):
        return obj.titulo[:60]


@admin.register(EstrategiaMensual)
class EstrategiaMensualAdmin(admin.ModelAdmin):
    list_display = ["empresa", "frecuencia_publicacion", "fecha_creacion"]
    list_filter = ["fecha_creacion"]
    search_fields = ["empresa__nombre_empresa", "objetivo", "pilares_contenido"]
    readonly_fields = ["fecha_creacion"]
    raw_id_fields = ["empresa"]


def _regenerar_action(modeladmin, request, queryset):
    from nexa.services.agentes.agente_diseno_instagram import generar_creatividad
    ok, errores = 0, 0
    for cr in queryset.select_related("contenido__empresa"):
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
            cr.save(update_fields=[
                "prompt_visual", "estructura_visual_json",
                "render_html", "render_css", "estado", "estilo", "estilo_nombre",
            ])
            ok += 1
        except Exception as exc:
            modeladmin.message_user(request, f"Error en {cr}: {exc}", level="error")
            errores += 1
    if ok:
        modeladmin.message_user(request, f"✅ {ok} creatividad(es) regenerada(s) con nuevos estilos.")

_regenerar_action.short_description = "🔄 Regenerar con nuevos estilos visuales"


@admin.register(CreatividadInstagram)
class CreatividadInstagramAdmin(admin.ModelAdmin):
    list_display  = ["__str__", "tipo", "estilo_nombre", "estado", "veces_regenerada", "fecha_creacion"]
    list_filter   = ["tipo", "estado", "estilo", "fecha_creacion"]
    search_fields = ["contenido__titulo", "contenido__empresa__nombre_empresa", "prompt_visual", "estilo_nombre"]
    readonly_fields = ["fecha_creacion", "veces_regenerada"]
    list_editable = ["estado"]
    raw_id_fields = ["contenido"]
    actions       = [_regenerar_action]
