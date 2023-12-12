from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from Model.models import Produit, Commande, Paniers


def panier(request):
    panier_utilisateur = Paniers.objects.filter(client=request.user, confirmation_panier=False).first()

    if panier_utilisateur:
        if request.method == 'POST':
            if 'mise_a_jour' in request.POST:
                for commande in panier_utilisateur.ordre.all():
                    nouvelle_quantite = request.POST.get(f'quantite-{commande.id}')
                    if nouvelle_quantite:
                        commande.quantite = nouvelle_quantite
                        commande.save()

            elif 'confirmer_commande' in request.POST:
                montant_total = panier_utilisateur.calculer_montant_total()
                panier_utilisateur.confirmation_panier = True
                panier_utilisateur.montant_total = montant_total
                panier_utilisateur.save()
                return redirect('vitrine:panier_confirme')

        return render(request, 'PanierContent.html', {'panier_utilisateur': panier_utilisateur})
    else:
        return render(request, 'PanierContent.html')

def suppprimer_panier(request):
    panie = request.user.



def liste_tous_produits(request):
    # Récupérer tous les produits
    tous_les_produits = Produit.objects.all()
    # for produit in tous_les_produits:
    #     # Vérifier s'il y a une promotion
    #     if produit.promotion:
    #         produit.prix_reduits = produit.prix - (produit.prix * produit.pourcentage_promotion / 100)
    #     else:
    #         produit.prix_reduits = produit.prix

    context = {'tous_les_produits': tous_les_produits}
    return render(request, 'products.html', context)


@login_required
def commander_produit(request):
    produit_id = request.POST.get('produit_id')
    quantite = request.POST.get('quantite')
    quantit = int(quantite)
    produit = get_object_or_404(Produit, pk=produit_id)
    prix = produit.get_prix_reduit() * quantit
    # Créer la commande avec le produit et la quantité
    commande = Commande.objects.create(
        client=request.user,
        quantite=quantit,
        montant_total=prix,  # Utilisez la méthode get_prix_reduit
        confirmer=False,
        statut='En attente'
    )

    # Ajouter le produit à la commande
    commande.produits.add(produit)

    response_data = {'message': 'Commande enregistrée avec succès!'}

    return JsonResponse(response_data)


def Accueil(request):
    return render(request, 'index.html')


def Contact(request):
    return render(request, 'contact.html')


def Faq(request):
    return render(request, 'faq.html')


def About(request):
    return render(request, 'about.html')


def produit_details(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)

    context = {'produit': produit}
    return render(request, 'product-detail.html', context)


def ajouter_panier(request, produit_id):
    user = request.user
    product = get_object_or_404(Produit, pk=produit_id)
    panier, _ = Paniers.objects.get_or_create(client=user)
    commande, cree = Commande.objects.get_or_create(client=user, produits=product)

    if cree:
        panier.ordre.add(commande)
        panier.save()
    else:
        commande.quantite += 1
        commande.save()
    return redirect(reverse("vitrine:Produit_details", kwargs={"produit_id": produit_id}))
