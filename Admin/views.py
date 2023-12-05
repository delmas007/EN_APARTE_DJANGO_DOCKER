from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Employer.forms import ConfirmationReservationForm
from Model.models import Rendez_vous


# Create your views here.

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
