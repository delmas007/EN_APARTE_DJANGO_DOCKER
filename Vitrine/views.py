from django.shortcuts import render

from Model.models import Produit


# Create your views here.

def liste_tous_produits(request):
    # Récupérer tous les produits
    tous_les_produits = Produit.objects.all()
    for produit in tous_les_produits:
        # Vérifier s'il y a une promotion
        if produit.promotion:
            produit.prix_reduit = produit.prix - (produit.prix * produit.pourcentage_promotion / 100)
        else:
            produit.prix_reduit = produit.prix

    context = {'tous_les_produits': tous_les_produits}
    return render(request, 'products.html', context)


def Accueil(request):
    return render(request, 'index.html')


def Contact(request):
    return render(request, 'contact.html')


def Faq(request):
    return render(request, 'faq.html')


def About(request):
    return render(request, 'about.html')


def Produitdetails(request):
    return render(request, 'product-detail.html')
