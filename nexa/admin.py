from django.contrib import admin
from .models import EmpresaNexa, MemoriaMarca, ContenidoGenerado, EstrategiaMensual


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
