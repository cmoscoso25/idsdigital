from django.urls import path
from billing import views

app_name = "billing"

urlpatterns = [
    path("", views.billing_dashboard, name="dashboard"),
    path("checkout/<int:plan_id>/", views.checkout_redirect, name="checkout"),
    path("exito/", views.checkout_success, name="exito"),
    path("cancelar/", views.checkout_cancel, name="cancelar"),
]
