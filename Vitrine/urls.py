from django.urls import path

from .views import Accueil, Contact, Faq, About, liste_tous_produits, produit_details, commander_produit, ajouter_panier

app_name = 'vitrine'

urlpatterns = [

    path('Contact/', Contact, name='Contact'),
    path('Faq/', Faq, name='Faq'),
    path('Accueil/', Accueil, name='Accueil'),
    path('A propos/', About, name='About'),
    path('liste_tous_produits/', liste_tous_produits, name='liste_tous_produits'),
    path('produit/<int:produit_id>/', produit_details, name='Produit_details'),
    path('produits/<int:produit_id>/ajouter', ajouter_panier, name='panier'),
    path('commander_produit/', commander_produit, name='commander_produit'),
]
