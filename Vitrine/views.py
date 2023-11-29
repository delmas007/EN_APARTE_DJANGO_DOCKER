from django.shortcuts import render


# Create your views here.
def Accueil(request):
    return render(request, 'index.html')


def Contact(request):
    return render(request, 'contact.html')


def Faq(request):
    return render(request, 'faq.html')

