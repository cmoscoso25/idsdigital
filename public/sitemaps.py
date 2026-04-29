from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "services_public",
            "automation_processes_public",
            "custom_software_development_public",
            "ai_solutions_public",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            "home": 1.0,
            "services_public": 0.9,
            "automation_processes_public": 0.9,
            "custom_software_development_public": 0.9,
            "ai_solutions_public": 0.9,
        }
        return priorities.get(item, 0.8)