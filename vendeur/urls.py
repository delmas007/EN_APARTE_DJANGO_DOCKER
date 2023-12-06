from django.urls import path
from vendeur.views import ajouter_produit

app_name = 'vendeur'
urlpatterns = [
    path('ajouter_un_produit/', ajouter_produit, name='ajouter_un_produit'),
]