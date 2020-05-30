from django.urls import path
from django.contrib.sitemaps.views import sitemap

from .sitemaps import ViewSitemap
from . import views

sitemaps = {
    'static': ViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #path('', views.indexMaintenance, name='indexMaintenance'), #! Ligne a décommenter pour une maintenance
    #""" 
    path('', views.index, name='index'),
    path('matchs/calendrier', views.indexCalendrier, name='indexCalendrier'),
    path('matchs/live', views.indexLive, name='indexLive'),
    path('matchs/results', views.indexResults, name='indexResults'),
    path('matchs/calendrier/<comp>', views.calendrierMatches, name='calendrierMatches'),
    path('matchs/live/<comp>', views.live, name='live'),
    path('matchs/results/<comp>', views.resultsMatches, name='results')
#""""
]