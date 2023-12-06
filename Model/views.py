from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from Model.forms import ConnexionForm, UserRegistrationForm, RendezVousForm
from Model.models import Roles


# Create your views here.

class Connexion(LoginView):
    template_name = 'connexion.html'
    form_class = ConnexionForm

    def get_success_url(self) -> str:
        if self.request.user.roles.role == 'EMPLOYER':
            return reverse('employer:reservation')
        elif self.request.user.roles.role == 'ADMIN':
            return reverse('admins:reservation_D')
        elif self.request.user.roles.role == 'CLIENT':
            return reverse('Accueil')
        elif self.request.user.roles.role == 'VENDEUR':
            return reverse('vendeur:ajouter_un_produit')


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


@csrf_protect
def Rendez_vous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save(commit=False)
            rendez_vous.client = request.user
            rendez_vous.save()
            return redirect('votre_vue_de_confirmation')
    else:
        form = RendezVousForm()
    return render(request, 'PageRendeVous.html', {'form': form})


class Deconnexion(LogoutView):
    pass
