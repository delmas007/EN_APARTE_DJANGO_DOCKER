from django.urls import path

from .views import Accueil, Contact, Faq, About, liste_tous_produits, produit_details, \
    ajouter_panier, commander_produit, panier, supprimer_element_panier, supprimer_panier

app_name = 'vitrine'

urlpatterns = [
    path('Accueil/', Accueil, name='Accueil'),
    path('About/', About, name='About'),
    path('Faq/', Faq, name='Faq'),
    path('Contact/', Contact, name='Contact'),
    path('liste_tous_produits/', liste_tous_produits, name='liste_tous_produits'),
    path('produit/<int:produit_id>/', produit_details, name='Produit_details'),
    path('produits/<int:produit_id>/ajouter', ajouter_panier, name='panier'),
    path('commander_produit/', commander_produit, name='commander_produit'),
    path('Panier/', panier, name='panier_confirme'),
    path('supprimer_element_panier/<int:commande_id>/', supprimer_element_panier, name='supprimer_element_panier'),
    path('supprimer_panier/', supprimer_panier, name='supprimer_panier'),
]


