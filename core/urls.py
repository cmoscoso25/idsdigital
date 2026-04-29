from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/solicitud/", views.api_crear_solicitud, name="api_crear_solicitud"),
]