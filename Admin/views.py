from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from Employer.forms import ConfirmationReservationForm
from Model.models import Rendez_vous


# Create your views here.
@login_required
def filtrer_rendez_vous(request):
    if not request.user.roles or request.user.roles.role != 'ADMIN':
        return redirect('Accueil')
    # Obtenez la liste de tous les rendez-vous
    tous_les_rendez_vous = Rendez_vous.objects.all()

    # Gestion des filtres
    date_filtre = request.GET.get('date', '')
    employer_filtre = request.GET.get('employer', '')
    client_filtre = request.GET.get('client', '')

    # Appliquer les filtres
    if date_filtre:
        tous_les_rendez_vous = tous_les_rendez_vous.filter(date_rendez_vous=date_filtre)
    if employer_filtre:
        tous_les_rendez_vous = tous_les_rendez_vous.filter(employer__nom__icontains=employer_filtre)
    if client_filtre:
        tous_les_rendez_vous = tous_les_rendez_vous.filter(client__nom__icontains=client_filtre)

    context = {
        'tous_les_rendez_vous': tous_les_rendez_vous,
        'date_filtre': date_filtre,
        'employer_filtre': employer_filtre,
        'client_filtre': client_filtre,
    }
    return render(request, 'rendez_vous_auj.html', context)

@login_required
def reservations_en_attente_D(request):
    if not request.user.roles or request.user.roles.role != 'ADMIN':
        return redirect('Accueil')

    reservations = Rendez_vous.objects.filter(en_attente=True, confirmation=False)

    if request.method == 'POST':
        form = ConfirmationReservationForm(request.POST)

        if form.is_valid():
            reservation_id = form.cleaned_data['reservation_id']
            confirmation = form.cleaned_data['confirmation']

            reservation = get_object_or_404(Rendez_vous, id=reservation_id)

            # Mettez à jour le champ de confirmation
            reservation.confirmation = True

            # Si la réservation est confirmée, enregistrez l'id de l'utilisateur connecté comme client
            if reservation.confirmation:
                reservation.employer = request.user
                reservation.en_attente = False

            reservation.save()

            # Ajoutez d'autres logiques pour le refus de la réservation si nécessaire
            # ...

            return redirect('employer:reservation')
    else:
        form = ConfirmationReservationForm()

    return render(request, 'indexe_D.html', {'reservations': reservations, 'form': form})


def reservations_confirmer_D(request):
    if not request.user.roles or request.user.roles.role != 'ADMIN':
        return redirect('Accueil')
    rendez_vous = Rendez_vous.objects.filter(confirmation=True, en_attente=False, fin=False, debut=False, employer=request.user.id)
    return render(request, 'indexe2_D.html', {'reservations': rendez_vous})


def rendez_vous_aujourdhui(request):
    # Obtenez la date actuelle
    today = timezone.now().date()

    # Filtrez les rendez-vous d'aujourd'hui
    rendez_vous_aujourdhui = Rendez_vous.objects.filter(
        date_rendez_vous=today
    )

    # Calculez l'état de chaque rendez-vous
    for rendez_vous in rendez_vous_aujourdhui:
        current_datetime = timezone.now()
        if rendez_vous.heure_debut_rendez_vous is not None and rendez_vous.heure_debut_rendez_vous <= current_datetime.time():
            rendez_vous.etat = "Commencé"
        elif rendez_vous.heure_fin_rendez_vous is not None and rendez_vous.heure_fin_rendez_vous <= current_datetime.time():
            rendez_vous.etat = "Terminé"
        else:
            rendez_vous.etat = "Pas encore commencé"

    context = {'rendez_vous_aujourdhui': rendez_vous_aujourdhui}
    return render(request, 'rendez_vous_auj.html', context)
