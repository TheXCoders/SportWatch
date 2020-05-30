from django.contrib import sitemaps
from django.urls import reverse

class ViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['index', 'indexCalendrier', 'indexLive', 'indexResults']

    def location(self, item):
        return reverse(item)
