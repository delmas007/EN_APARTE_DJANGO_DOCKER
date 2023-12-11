from django.urls import path

from .views import Accueil, Contact, Faq, About, Produitdetails, liste_tous_produits

app_name = 'vitrine'

urlpatterns = [

    path('Contact/', Contact, name='Contact'),
    path('Faq/', Faq, name='Faq'),
    path('Accueil/', Accueil, name='Accueil'),
    path('A propos/', About, name='About'),
    path('Produit details/', Produitdetails, name='Produit details'),
    path('liste_tous_produits/', liste_tous_produits, name='liste_tous_produits'),
]
