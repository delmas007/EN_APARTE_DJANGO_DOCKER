from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from Model.forms import ConnexionForm, UserRegistrationForm, RendezVousForm
from Model.models import Roles, Service, Utilisateur
from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from Model.tokens import account_activation_token



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


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Utilisateur.objects.get(mon_uuid=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can log in to your account.")
        return redirect('Model:connexion')
    else:
        messages.error(request, "Activation link is invalid or user not found!")

    return redirect('Accueil')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    print(f'user {user.mon_uuid}')
    message = render_to_string("template_activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.mon_uuid)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user.nom}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@csrf_protect
def inscription(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.get_email_field_name)
            client_role = Roles.objects.get(role=Roles.CLIENT)
            user.roles = client_role
            user.is_active = False
            activateEmail(request, user, form.cleaned_data.get('email'))
            user.save()
            return redirect('Model:connexion')
        else:
            context['form'] = form  # Passez le formulaire de retour au modèle avec les erreurs

    form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'inscription.html', context=context)

@csrf_protect
def Rendez_vous(request):
    services = Service.objects.all()
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save(commit=False)
            rendez_vous.client = request.user
            rendez_vous.save()
            return redirect('votre_vue_de_confirmation')
    else:
        form = RendezVousForm()
    return render(request, 'PageRendeVous.html', {'form': form, 'services': services})


class Deconnexion(LogoutView):
    pass
