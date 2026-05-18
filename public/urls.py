from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("demo/", views.submit_demo_request, name="submit_demo"),

    # Blog
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
]