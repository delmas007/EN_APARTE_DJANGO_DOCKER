
from django.urls import path
from .views import rendez_vous_aujourdhui, reservations_en_attente_D, reservations_confirmer_D, filtrer_rendez_vous, \
    inscription_D, active_emp, desactive_amp, employer_compte, liste_produits_D, liste_paniers_confirmes_D, \
    liste_paniers_traitements_D, liste_commandes_receptionnees_D, filtrer_Commande, produit_log_list, ajout_service, \
    liste_services, supprimer_service, modifier_service, liste_services_mode

app_name = 'admins'
urlpatterns = [
    path('Inscription/', inscription_D, name='inscription_D'),
    path('Rendez-vous-aujourdhui/', rendez_vous_aujourdhui, name='rendez_vous_aujourdhui'),
    path('Reservation_D/', reservations_en_attente_D, name='reservation_D'),
    path('Reservations_confirmer_D/', reservations_confirmer_D, name='reservation_confirmer_D'),
    path('Filtrer-rendez-vous/', filtrer_rendez_vous, name='filtrer_rendez_vous'),
    path('Filtrer_Commande/', filtrer_Commande, name='filtrer_Commande'),
    path('Active_employer/<int:employer_id>/', active_emp, name='active_emp'),
    path('Desactive_employer/<int:employer_id>/', desactive_amp, name='desactive_amp'),
    path('Compte_employer/', employer_compte, name='Compte_employer'),
    path('Liste_produits/', liste_produits_D, name='List_produit'),
    path('liste_paniers_confirmes/', liste_paniers_confirmes_D, name='liste_paniers_confirmes'),
    path('liste_paniers_traitements/', liste_paniers_traitements_D, name='liste_paniers_traitements'),
    path('liste_commandes_receptionnees/', liste_commandes_receptionnees_D, name='liste_commandes_receptionnees'),
    path('logs-produits/', produit_log_list, name='produit_log_list'),
    path('ajout-service/', ajout_service, name='ajout_service'),
    path('liste-services/', liste_services, name='liste_services'),
    path('supprimer-service/<int:service_id>/', supprimer_service, name='supprimer_service'),
    path('liste-services-modifier/', liste_services_mode, name='liste_services_mode'),
    path('modifier_service/<int:service_id>/', modifier_service, name='modifier_service'),
]