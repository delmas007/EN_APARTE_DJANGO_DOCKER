
from django.urls import path
from .views import rendez_vous_aujourdhui, reservations_en_attente_D, reservations_confirmer_D, filtrer_rendez_vous, \
    inscription_D

app_name = 'admin'
urlpatterns = [
    path('Inscription/', inscription_D, name='inscription_D'),
    path('rendez-vous-aujourdhui/', rendez_vous_aujourdhui, name='rendez_vous_aujourdhui'),
    path('reservation_D/', reservations_en_attente_D, name='reservation_D'),
    path('reservations_confirmer_D/', reservations_confirmer_D, name='reservation_confirmer_D'),
    path('filtrer-rendez-vous/', filtrer_rendez_vous, name='filtrer_rendez_vous'),
]