from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return [
            # PRINCIPAL
            "home",

            # CORE
            "services_public",
            "automation_processes_public",
            "custom_software_development_public",
            "ai_solutions_public",

            # SEO CLUSTER NUEVO
            "software_empresas_chile",
            "sistemas_gestion_empresarial_chile",
            "automatizacion_python_empresas",
            "dashboards_empresariales_chile",
            "inteligencia_artificial_empresas_chile",
            "desarrollo_sistemas_internos",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        prioridades = {
            "home": 1.0,

            "services_public": 0.9,
            "automation_processes_public": 0.9,
            "custom_software_development_public": 0.9,
            "ai_solutions_public": 0.9,

            "software_empresas_chile": 0.8,
            "sistemas_gestion_empresarial_chile": 0.8,
            "automatizacion_python_empresas": 0.8,
            "dashboards_empresariales_chile": 0.8,
            "inteligencia_artificial_empresas_chile": 0.8,
            "desarrollo_sistemas_internos": 0.8,
        }
        return prioridades.get(item, 0.7)