from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from Model.models import Roles, Produit
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


@login_required
def liste_produits(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    produits = Produit.objects.all()
    return render(request, 'list_PO.html', {'produits': produits})


@login_required
def modifier_produit(request, produit_id):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        form = UserRegistrationFormee(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifier avec succès !')
    else:
        form = UserRegistrationFormee(instance=produit)

    return render(request, 'produit_M.html', {'form': form, 'produit': produit})


@login_required
def supprimer_produit(request, produit_id):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    produit = get_object_or_404(Produit, id=produit_id)
    produit.delete()
    messages.success(request, 'Produit supprimé avec succès !')
    return redirect('vendeur:liste_produits')
