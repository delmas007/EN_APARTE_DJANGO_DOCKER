from django.shortcuts import render


# Create your views here.
def Accueil(request):
    return render(request, 'index.html')


def Contact(request):
    return render(request, 'contact.html')


def Faq(request):
    return render(request, 'faq.html')


def Produit(request):
    return render(request, 'products.html')


def About(request):
    return render(request, 'about.html')


def Produitdetails(request):
    return render(request, 'product-detail.html')
