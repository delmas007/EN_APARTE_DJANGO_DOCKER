from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from Model.models import Roles
from vendeur.forms import UserRegistrationFormee


# Create your views here.
@csrf_protect
@login_required
def ajouter_produit(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    context = {}
    if request.method == 'POST':
        form = UserRegistrationFormee(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit ajouter avec succès !')
        else:
            context['errors'] = form.errors

    form = UserRegistrationFormee()
    context['form'] = form
    return render(request, 'produit_A.html', context=context)