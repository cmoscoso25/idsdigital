from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("demo/", views.submit_demo_request, name="submit_demo"),
    path("servicios/", views.services, name="services"),
    path("automatizacion-procesos/", views.automation_processes, name="automation_processes"),
    path("desarrollo-software-medida/", views.custom_software_development, name="custom_software_development"),
    path("inteligencia-artificial-empresas/", views.ai_solutions, name="ai_solutions"),
]