from django.urls import path
from vendeur.views import ajouter_produit, liste_produits, modifier_produit, supprimer_produit

app_name = 'vendeur'
urlpatterns = [
    path('ajouter_un_produit/', ajouter_produit, name='ajouter_un_produit'),
    path('liste_produits/', liste_produits, name='liste_produits'),
    path('modifier_produit/<int:produit_id>/', modifier_produit, name='modifier_produit'),
    path('produits/<int:produit_id>/supprimer/', supprimer_produit, name='supprimer_produit'),
]
