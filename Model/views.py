from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
from Model.forms import ConnexionForm, UserRegistrationForm, RendezVousForm, PasswordResetForme, ChangerMotDePasse, \
    EvaluationForm
from Model.models import Roles, Service, Utilisateur, Rendez_vous
from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.templatetags.static import static

from Model.token import account_activation_tokens
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
        messages.success(request, "Merci de votre confirmation par courriel. Vous pouvez maintenant vous connecter à "
                                  "votre compte.")
        return redirect('Model:connexion')
    else:
        messages.error(request, "Le lien d’activation est invalide !")

    return redirect('Model:connexion')


def activateEmail(request, user, to_email):
    mail_subject = "Activez votre compte utilisateur."
    message = render_to_string("new-email.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.mon_uuid)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http',
        'logo': get_current_site(request).domain + static('image/photo_2023-12-14_15-44-58.ico')
    })
    plain_message = strip_tags(message)
    email = EmailMultiAlternatives(subject=mail_subject, body=plain_message, to=[to_email])
    email.attach_alternative(message, "text/html")
    email.send()
    if email.send():
        messages.success(request, f'Cher <b>{user.nom}</b>, veuillez accéder à votre boîte de réception <b>{to_email}"'
                                  f'</b> et cliquer sur le lien d’activation reçu pour confirmer et compléter '
                                  f'l’enregistrement. <b>Remarque :</b>  Vérifiez votre dossier spam.')
    else:
        messages.error(request,
                       f'Problème d’envoi du courriel à {to_email}, vérifiez si vous l’avez saisi correctement.')


@csrf_protect
def inscription(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            client_role = Roles.objects.get(role=Roles.CLIENT)
            user.roles = client_role
            user.is_active = False
            activateEmail(request, user, form.cleaned_data.get('email'))
            user.save()
            return redirect('Model:connexion')
        else:

            context['form'] = form
            return render(request, 'inscription.html', context=context)

    form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'inscription.html', context=context)


@csrf_protect
def Rendez_vouss(request):
    services = Service.objects.all()
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save(commit=False)
            rendez_vous.client = request.user
            rendez_vous.save()
            messages.success(request, 'Votre rendez-vous a été pris avec succès. Merci !')
            return redirect('Model:Rendez_vous')
    else:
        form = RendezVousForm()

    return render(request, 'PageRendeVous.html', {'form': form, 'services': services})


class Deconnexion(LogoutView):
    pass


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForme(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("reinitialisation.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.mon_uuid)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                plain_message = strip_tags(message)
                email = EmailMultiAlternatives(subject=subject, body=plain_message, to=[associated_user.email])
                email.attach_alternative(message, "text/html")
                email.send()
                if email.send():
                    messages.success(request,
                                     """
                                     <h4>Réinitialisation du mot de passe envoyée</h4><hr>
                                     <p>
                                         Nous vous avons envoyé les instructions par e-mail pour définir votre mot de passe. Si un compte existe avec l’e-mail que vous avez entré,
                                          vous devriez les recevoir sous peu. <br>Si vous ne recevez pas le courriel, veuillez vous assurer d’avoir saisi l’adresse e-mail avec 
                                          laquelle vous vous êtes inscrit(e) et vérifiez votre dossier spam.
                                     </p>
                                     """
                                     )
                else:
                    messages.error(request, "Problème d’envoi de l’e-mail de réinitialisation du mot de passe, "
                                            "<b>PROBLÈME SERVEUR</b>")

            return redirect('Model:connexion')

    form = PasswordResetForme()
    return render(
        request=request,
        template_name="email.html",
        context={"form": form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(mon_uuid=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ChangerMotDePasse(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été défini. Vous pouvez continuer et <b>vous "
                                          "connecter </b> maintenant.")
                return redirect('Model:connexion')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = ChangerMotDePasse(user)
        return render(request, 'password.html', {'form': form})
    else:
        messages.error(request, "Le lien a expiré")

    messages.error(request, 'Quelque chose a mal tourné, rediriger vers la page d’accueil')
    return redirect("Accueil")


def evaluations(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        Rendez_Vous = Rendez_vous.objects.get(eva_uuid=uid)
    except:
        Rendez_Vous = None

    if Rendez_Vous is not None and account_activation_tokens.check_token(Rendez_Vous, token):
        if request.method == 'POST':
            form = EvaluationForm(request.POST,instance=Rendez_Vous)
            if form.is_valid():
                form.save()
                messages.success(request, "Nous tenons à exprimer notre gratitude pour votre évaluation. Votre "
                                          "feedback est essentiel pour nous et nous aide à offrir un service toujours "
                                          "meilleur. Merci de choisir notre entreprise, nous sommes ravis de vous "
                                          "compter parmi nos clients. À bientôt !")
        form = EvaluationForm()
        return render(request, 'note.html', {'form': form})
    else:
        messages.error(request, "Le lien a expiré")
    messages.error(request, 'Quelque chose a mal tourné, rediriger vers la page d’accueil')
    form = EvaluationForm()
    return render(request, 'note.html', {'form': form})


def evaluation_email(request, mail, rendez_vous_uuid):
    associated_user = get_user_model().objects.filter(Q(email=mail)).first()
    uuid = Rendez_vous.objects.filter(Q(eva_uuid=rendez_vous_uuid)).first()
    if uuid:
        subject = "Votre Avis Nous Importe - Évaluez notre Service"
        message = render_to_string("evaluation.html", {
            'user': associated_user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(rendez_vous_uuid)),
            'token': account_activation_tokens.make_token(uuid),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        plain_message = strip_tags(message)
        email = EmailMultiAlternatives(subject=subject, body=plain_message, to=[associated_user.email])
        email.attach_alternative(message, "text/html")
        email.send()
