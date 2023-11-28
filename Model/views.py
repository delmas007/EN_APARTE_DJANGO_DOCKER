from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from Model.forms import ConnexionForm, UserRegistrationForm
from Model.models import Roles


# Create your views here.

class Connexion(LoginView):
    template_name = 'connexion.html'
    form_class = ConnexionForm


@csrf_protect
def inscription(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            client_role = Roles.objects.get(role=Roles.CLIENT)
            user.roles = client_role

            user.save()
            return redirect('Model:connexion')
        else:
            context['errors'] = form.errors

    form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'inscription.html', context=context)
