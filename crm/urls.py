from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("leads/", views.lead_list, name="lead_list"),
    path("leads/<int:lead_id>/", views.lead_detail, name="lead_detail"),
    path("leads/<int:lead_id>/estado/", views.lead_change_status, name="lead_change_status"),

    path("solicitudes/", views.demorequest_list, name="demorequest_list"),
    path("solicitudes/<int:request_id>/", views.demorequest_detail, name="demorequest_detail"),
    path("solicitudes/<int:request_id>/convertir/", views.demorequest_convert, name="demorequest_convert"),
    path("solicitudes/<int:request_id>/archivar/", views.demorequest_archive, name="demorequest_archive"),
]