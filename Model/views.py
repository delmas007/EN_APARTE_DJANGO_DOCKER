from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.

class Connexion(LoginView):
    template_name = 'Model/connexion.html'
    form_class = ConnexionForm

    def get_success_url(self) -> str:
        b = super().get_success_url()
        if self.request.user.admins == True:
            return reverse('base:bienvenue')
        elif self.request.user.admins == False:
            return b