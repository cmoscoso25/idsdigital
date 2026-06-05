from django.urls import path
from . import views

app_name = "nexa"

urlpatterns = [
    path("app/", views.dashboard, name="dashboard"),
    path("app/empresas/", views.empresa_list, name="empresa_list"),
    path("app/empresas/nueva/", views.empresa_nueva, name="empresa_nueva"),
    path("app/empresas/<int:pk>/", views.empresa_detalle, name="empresa_detalle"),
    path("app/empresas/<int:pk>/memoria/", views.memoria_editar, name="memoria_editar"),
    path("app/empresas/<int:pk>/generar/", views.generar, name="generar"),
    path("app/contenidos/", views.contenido_list, name="contenido_list"),
    path("app/contenidos/<int:pk>/", views.contenido_detalle, name="contenido_detalle"),
    path("app/estrategias/", views.estrategia_list, name="estrategia_list"),
    path("app/empresas/<int:pk>/estrategia/", views.estrategia_nueva, name="estrategia_nueva"),
    path("app/estrategias/<int:pk>/", views.estrategia_detalle, name="estrategia_detalle"),
    path("app/estrategias/<int:pk>/generar/", views.generar_contenido_mes, name="generar_contenido_mes"),
    path("app/creatividades/", views.creatividad_list, name="creatividad_list"),
    path("app/contenidos/<int:contenido_pk>/creatividad/", views.generar_creatividad_view, name="generar_creatividad"),
    path("app/creatividades/<int:pk>/", views.creatividad_detalle, name="creatividad_detalle"),
    path("app/creatividades/<int:creatividad_pk>/regenerar/", views.regenerar_creatividad_view, name="regenerar_creatividad"),
    path("app/creatividades/<int:creatividad_pk>/imagen/", views.generar_imagen_ia_view, name="generar_imagen_ia"),
]
