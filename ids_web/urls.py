from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from public import views as public_views
from public.sitemaps import StaticViewSitemap
from core.views import health_check

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", public_views.landing, name="home"),
    path("health/", health_check, name="health_check"),

    path("core/", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("panel/", include("crm.urls")),
    path("public/", include("public.urls")),
    path("agente-ia/", include("agente_ia.urls")),

    # Blog
    path("blog/", public_views.blog_list, name="blog_list_public"),
    path("blog/<slug:slug>/", public_views.blog_detail, name="blog_detail_public"),

    path("servicios/", public_views.services, name="services_public"),
    path("automatizacion-procesos/", public_views.automation_processes, name="automation_processes_public"),
    path("desarrollo-software-medida/", public_views.custom_software_development, name="custom_software_development_public"),
    path("inteligencia-artificial-empresas/", public_views.ai_solutions, name="ai_solutions_public"),

    path("software-para-empresas-chile/", public_views.software_empresas_chile, name="software_empresas_chile"),
    path("sistemas-gestion-empresarial-chile/", public_views.sistemas_gestion_empresarial_chile, name="sistemas_gestion_empresarial_chile"),
    path("automatizacion-python-empresas/", public_views.automatizacion_python_empresas, name="automatizacion_python_empresas"),
    path("dashboards-empresariales-chile/", public_views.dashboards_empresariales_chile, name="dashboards_empresariales_chile"),
    path("inteligencia-artificial-empresas-chile/", public_views.inteligencia_artificial_empresas_chile, name="inteligencia_artificial_empresas_chile"),
    path("desarrollo-sistemas-internos/", public_views.desarrollo_sistemas_internos, name="desarrollo_sistemas_internos"),

    path("nexa/", public_views.nexa, name="nexa_public"),
    path("nexa/", include("nexa.urls")),

    path("robots.txt", public_views.robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)