from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from public import views as public_views
from public.sitemaps import StaticViewSitemap

# 👇 IMPORTANTE
from core.views import health_check

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", public_views.landing, name="home"),

    # 🔥 HEALTH CHECK EN RAÍZ
    path("health/", health_check, name="health_check"),

    # Apps
    path("core/", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("panel/", include("crm.urls")),
    path("public/", include("public.urls")),

    # Públicas
    path("servicios/", public_views.services, name="services_public"),
    path("automatizacion-procesos/", public_views.automation_processes, name="automation_processes_public"),
    path("desarrollo-software-medida/", public_views.custom_software_development, name="custom_software_development_public"),
    path("inteligencia-artificial-empresas/", public_views.ai_solutions, name="ai_solutions_public"),

    # SEO
    path("robots.txt", public_views.robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)