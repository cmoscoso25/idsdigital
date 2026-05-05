from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("demo/", views.submit_demo_request, name="submit_demo"),
]