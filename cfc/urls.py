from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="cfc_home"),
    path("favorable", views.favorable, name="cfc_favorable"),
    path("non_favorable", views.non_favorable, name="cfc_nom_favorable"),
    path("non_traite", views.non_traite, name="cfc_non_traite"),
    path('Validate/<demandeur_slug>', views.Validate, name = 'cfc_validate'),
    path('custum/<demandeur_slug>' , views.custum, name = 'cfc_custum'),


]
