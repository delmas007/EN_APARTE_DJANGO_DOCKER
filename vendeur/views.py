from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
from django.views import View
from datetime import datetime, timedelta
from Model.models import Roles, Produit, Paniers
from vendeur.forms import UserRegistrationFormee, UserRegistrationFor


# Create your views here.
@csrf_protect
@login_required(login_url='')
def ajouter_produit(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')

    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()
    p = 1

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
    }

    if request.method == 'POST':
        # Associez l'utilisateur connecté à la partie employer du formulaire
        form = UserRegistrationFormee(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.employer = request.user
            produit.save()
            messages.success(request, 'Produit ajouté avec succès !')
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
    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()
    p = 1

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'produits': produits
    }
    return render(request, 'list_PO.html', context)


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

    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()
    p = 1

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'form': form, 'produit': produit
    }

    return render(request, 'produit_M.html', context)


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
    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'produits': produits
    }

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
    paniers_confirmes = Paniers.objects.filter(confirmation_panier=True, confirmation_employer=False)

    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'paniers_confirmes': paniers_confirmes
    }

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

    send_confirmation_email(panier.client.email, panier)

    for commande in panier.ordre.all():
        print(f"Produit: {{commande.produits.nom}}, Quantité: {{commande.quantite}}, Prix unitaire: {commande.produits.get_prix_reduit}")
        print(f"Sous-total: {commande.quantite * commande.produits.prix}")

# Imprimer le prix total
    print(f"Prix total du panier: {{panier.montant_total}}")

    return redirect('vendeur:liste_paniers_confirmes')


def send_confirmation_email(client_email, panier):
    subject = 'Confirmation de commande EN APARTE'
    message = render_to_string('email_C.html', {'panier': panier})
    plain_message = strip_tags(message)
    recipient_list = [client_email]

    email = EmailMultiAlternatives(subject=subject, body=plain_message, to=recipient_list)
    email.attach_alternative(message, "text/html")
    email.send()


@login_required
def liste_paniers_traitements(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    paniers_traitements = Paniers.objects.filter(employer=request.user, confirmation_employer=True,
                                                 reception_commande=False)
    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'paniers_traitements': paniers_traitements
    }
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


@login_required
def liste_commandes_receptionnees(request):
    if not request.user.roles or request.user.roles.role != 'VENDEUR':
        return redirect('Accueil')
    commandes_receptionnees = Paniers.objects.filter(
        employer=request.user,
        reception_commande=True,
        date_reception_commande__date=date.today()
    )

    today = datetime.now()

    # Obtenez les produits pour chaque statut avec la date de réception correspondante
    produits_en_attente = Paniers.objects.filter(statut='En attente', confirmation_panier=True).count()
    produits_en_cours = Paniers.objects.filter(statut='En cours de traitement', employer=request.user).count()
    produits_expedies = Paniers.objects.filter(statut='Expédiée', date_reception_commande__date=today,
                                               employer=request.user).count()

    # Calculez le nombre total de produits
    total_produits = produits_en_attente + produits_en_cours + produits_expedies

    # Renvoyez ces valeurs dans le contexte pour les utiliser dans le template
    context = {
        'produits_en_attente': produits_en_attente,
        'produits_en_cours': produits_en_cours,
        'produits_expedies': produits_expedies,
        'total_produits': total_produits,
        'commandes_receptionnees': commandes_receptionnees
    }
    return render(request, 'panier_E.html', context)
