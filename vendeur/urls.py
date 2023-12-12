from django.urls import path
from vendeur.views import ajouter_produit, liste_produits, modifier_produit, supprimer_produit, toggle_promotion, \
    liste_produitss, liste_paniers_confirmes, confirmer_statut_panier

app_name = 'vendeur'
urlpatterns = [
    path('ajouter_un_produit/', ajouter_produit, name='ajouter_un_produit'),
    path('liste_produits/', liste_produits, name='liste_produits'),
    path('modifier_produit/<int:produit_id>/', modifier_produit, name='modifier_produit'),
    path('produits/<int:produit_id>/supprimer/', supprimer_produit, name='supprimer_produit'),
    path('produits/', liste_produitss, name='liste_produitss'),
    path('produit/<int:produit_id>/toggle_promotion/', toggle_promotion, name='toggle_promotion'),
    path('liste_paniers_confirmes/', liste_paniers_confirmes, name='liste_paniers_confirmes'),
    path('confirmer_statut_panier/<int:panier_id>/', confirmer_statut_panier, name='confirmer_statut_panier'),
]
