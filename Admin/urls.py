
from django.urls import path
from .views import rendez_vous_aujourdhui, reservations_en_attente_D, reservations_confirmer_D, filtrer_rendez_vous, \
    inscription_D, active_emp, desactive_amp, employer_compte

app_name = 'admins'
urlpatterns = [
    path('Inscription/', inscription_D, name='inscription_D'),
    path('Rendez-vous-aujourdhui/', rendez_vous_aujourdhui, name='rendez_vous_aujourdhui'),
    path('Reservation_D/', reservations_en_attente_D, name='reservation_D'),
    path('Reservations_confirmer_D/', reservations_confirmer_D, name='reservation_confirmer_D'),
    path('Filtrer-rendez-vous/', filtrer_rendez_vous, name='filtrer_rendez_vous'),
    path('Active_employer/<int:employer_id>/', active_emp, name='active_emp'),
    path('Desactive_employer/<int:employer_id>/', desactive_amp, name='desactive_amp'),
    path('Compte_employer/', employer_compte, name='Compte_employer'),
]