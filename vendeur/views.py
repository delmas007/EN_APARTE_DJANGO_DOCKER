from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from Model.models import Roles, Produit, Paniers
from vendeur.forms import UserRegistrationFormee, UserRegistrationFor


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
        form = UserRegistrationFor(request.POST, request.FILES, instance=produit)
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


@login_required
def liste_produitss(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    produits = Produit.objects.all()
    context = {'produits': produits}
    return render(request, 'promotion_V.html', context)


@login_required
def toggle_promotion(request, produit_id):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')

    produit = get_object_or_404(Produit, pk=produit_id)

    if request.method == 'POST':
        # Si le formulaire est soumis, traitez les données
        if 'pourcentage_promotion' in request.POST:
            pourcentage_promotion = request.POST.get('pourcentage_promotion')
            # Assurez-vous que pourcentage_promotion est un entier valide
            try:
                pourcentage_promotion = int(pourcentage_promotion)
                produit.pourcentage_promotion = pourcentage_promotion
            except ValueError:
                # Gérer l'erreur si pourcentage_promotion n'est pas un entier valide
                # Vous pouvez ajouter ici le comportement souhaité en cas d'erreur
                pass

        # Basculez la promotion entre True et False uniquement si le bouton correspondant est soumis
        elif 'toggle_promotion' in request.POST:
            produit.promotion = not produit.promotion

        produit.save()

    return redirect('vendeur:liste_produitss')


@login_required
def liste_paniers_confirmes(request):
    paniers_confirmes = Paniers.objects.filter(confirmation_panier=True , confirmation_employer=False)

    context = {'paniers_confirmes': paniers_confirmes}
    return render(request, 'panier_C.html', context)


@login_required
def confirmer_statut_panier(request, panier_id):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    panier = Paniers.objects.get(id=panier_id)

    if not panier.confirmation_employer:
        panier.confirmation_employer = True
        panier.statut = 'En cours de traitement'  # Mettez à jour le statut comme vous le souhaitez
        panier.employer = request.user  # Enregistrez l'utilisateur qui a effectué l'action
        panier.save()

        messages.success(request, 'Le statut du panier a été confirmé avec succès.')
    else:
        messages.warning(request, 'Le statut du panier a déjà été confirmé.')

    return redirect('vendeur:liste_paniers_confirmes')

@login_required
def liste_paniers_traitements(request):
    paniers_traitements = Paniers.objects.filter(employer=request.user,confirmation_employer=True, reception_commande= False)

    context = {'paniers_traitements': paniers_traitements}
    return render(request, 'panier_T.html', context)


@login_required
def confirmer_statut_traitements(request, panier_id):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    panier = Paniers.objects.get(id=panier_id)

    if not panier.reception_commande:
        panier.reception_commande = True
        panier.statut = 'Expédiée'
        panier.save()

        messages.success(request, 'Le statut du panier a été expédiée.')
    else:
        messages.warning(request, 'Le statut du panier a déjà été expédiée.')

    return redirect('vendeur:liste_paniers_traitements')
