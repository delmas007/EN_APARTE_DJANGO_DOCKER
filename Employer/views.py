from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from Employer.forms import ConfirmationReservationForm
from Model.models import Rendez_vous


# noinspection PyPackageRequirements
@login_required
def reservations_confirmer(request):
    if not request.user.roles or request.user.roles.role != 'EMPLOYER':
        return redirect('Accueil')
    rendez_vous = Rendez_vous.objects.filter(confirmation=True, en_attente=False,fin=False, employer=request.user.id)
    return render(request, 'indexe2.html', {'rendez_vous': rendez_vous})


@login_required
def debut_rendez_vous(request, rendez_vous_id):
    rdv = get_object_or_404(Rendez_vous, id=rendez_vous_id)

    # Mettre à jour le champ 'debut' à True
    rdv.debut = True
    rdv.save()

    return redirect('employer:reservation_confirmer')


@login_required
def fin_rendez_vous(request, rendez_vous_id):
    rdv = get_object_or_404(Rendez_vous, id=rendez_vous_id)

    # Mettre à jour le champ 'fin' à True
    rdv.fin = True
    rdv.save()

    return redirect('employer:reservation_confirmer')


@login_required
def reservations_en_attente(request):
    if not request.user.roles or request.user.roles.role != 'EMPLOYER':
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
            if confirmation:
                print(f"Réservation {reservation_id} confirmée par {request.user}")
            else:
                print(f"Réservation {reservation_id} refusée par {request.user}")

            # Ajoutez d'autres logiques pour le refus de la réservation si nécessaire
            # ...

            return redirect('employer:reservation')
    else:
        form = ConfirmationReservationForm()

    return render(request, 'indexe.html', {'reservations': reservations, 'form': form})

# Create your views here.
