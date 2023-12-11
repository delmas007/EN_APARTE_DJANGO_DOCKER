from django.urls import path

from .views import Accueil, Contact, Faq, Produit, About, liste_tous_produits, produit_details, \
    ajouter_panier, commander_produit

app_name = 'vitrine'

urlpatterns = [
    path('Accueil/', Accueil, name='Accueil'),
    path('A propos/', About, name='About'),
    path('liste_tous_produits/', liste_tous_produits, name='liste_tous_produits'),
    -    path('produit/<int:produit_id>/', produit_details, name='Produit details'),
    +    path('produit/<int:produit_id>/', produit_details, name='Produit_details'),
    +    path('produits/<int:produit_id>/ajouter', ajouter_panier, name='panier'),
    path('commander_produit/', commander_produit, name='commander_produit'),
]

