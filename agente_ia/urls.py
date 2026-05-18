from django.urls import path
from . import views

app_name = "agente_ia"

urlpatterns = [
    path("chat/", views.chat_diagnostico, name="chat_diagnostico"),
    path("guardar/", views.guardar_diagnostico, name="guardar_diagnostico"),
]