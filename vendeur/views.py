from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from Model.models import Roles
from vendeur.forms import UserRegistrationFormee


# Create your views here.
@csrf_protect
@login_required
def ajouter_produit(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationFormee(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            client_role = Roles.objects.get(role=Roles.EMPLOYER)
            user.roles = client_role

            user.save()
            messages.success(request, 'Employer ajouter avec succès !')
        else:
            context['errors'] = form.errors

    form = UserRegistrationFormee()
    context['form'] = form
    return render(request, 'produit_A.html', context=context)