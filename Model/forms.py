from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from django import forms
from Model.models import Utilisateur, Rendez_vous, horaire, Service


class ConnexionForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'type': "email",
            'class': "form-control",
            'style': "color: black;",
            'id': "email",
            'placeholder': "name@example.com",
            'required': '',
            'pattern': '[^ @]*@[^ @]*',
            'name': 'email',
        })
        self.fields['password'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'style': "color: black;",
            'id': "password",
            'placeholder': "Password",
        })


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'type': "email",
            'class': "form-control",
            'style': "color: black;",
            'id': "email",
            'placeholder': "name@example.com",
            'required': '',
            'pattern': '[^ @]*@[^ @]*',
            'name': 'email',
        })
        self.fields['nom'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'style': "color: black;",
            'id': "nom",
            'placeholder': "Nom",
            'required': '',
            'name': 'nom',
        })
        self.fields['prenom'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'style': "color: black;",
            'id': "prenom",
            'placeholder': "prenom",
            'required': '',
            'name': 'prenom',
        })
        self.fields['contact'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'style': "color: black;",
            'id': "contact",
            'placeholder': "0715226698",
            'required': '',
            'name': 'contact',
        })
        self.fields['commune'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'style': "color: black;",
            'id': "commune",
            'placeholder': "abidjan",
            'required': '',
            'name': 'commune',
        })
        self.fields['sexe'].widget.attrs.update({
            'name': "sexe",
            'style': "color: #212529;",
            'class': "form-select",
            'id': "sexe",
        })
        self.fields['password1'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'style': "color: black;",
            'id': "password",
            'placeholder': "Password",
        })
        self.fields['password2'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'style': "color: black;",
            'id': "password",
            'placeholder': "Confirme Password",
        })

    class Meta:
        model = Utilisateur
        fields = ('email', 'nom', 'prenom', 'contact', 'commune', 'sexe')


class XYZ_DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'w-full p-2 border border-gray-300 rounded',
            'required': 'True',
        })
        kwargs["format"] = "%m-%d-%Y"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = Rendez_vous
        fields = ['date_rendez_vous', 'service', 'horaire', 'preference_employer']

        widgets = {
            'date_rendez_vous': XYZ_DateInput(attrs={
                'id': 'id_date_rendez_vous',  # Utilisez l'ID généré par Django
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        service_disponibles = Service.objects.filter(disponibilite=True)

        # Récupérer les horaires déjà sélectionnés pour ce rendez-vous (si édité)
        service_selectionne = None
        if self.instance and self.instance.service:
            service_selectionne = self.instance.service

        # Filtrer les heures disponibles en fonction de l'horaire sélectionné (s'il existe)
        service_disponibles = service_disponibles.exclude(
            pk=service_selectionne.pk) if service_selectionne else service_disponibles

        # Mettre à jour les choix du champ 'horaire'
        self.fields['service'].queryset = service_disponibles

        # Mettre à jour les attributs du widget pour le champ 'horaire'
        self.fields['service'].widget.attrs.update({
            'class': 'form-control',
            'id': 'service',
            'required': True
        })

        self.fields['service'].widget.attrs.update({
            'name': 'reason',
            'class': 'form-control',
            'id': 'service',  # Utilisez l'ID généré par Django
            'required': True
        })

        # Horaire
        heures_disponibles = horaire.objects.filter(disponibilite=True)

        # Récupérer les horaires déjà sélectionnés pour ce rendez-vous (si édité)
        horaire_selectionne = None
        if self.instance and self.instance.horaire:
            horaire_selectionne = self.instance.horaire

        # Filtrer les heures disponibles en fonction de l'horaire sélectionné (s'il existe)
        heures_disponibles = heures_disponibles.exclude(
            pk=horaire_selectionne.pk) if horaire_selectionne else heures_disponibles

        # Mettre à jour les choix du champ 'horaire'
        self.fields['horaire'].queryset = heures_disponibles

        # Mettre à jour les attributs du widget pour le champ 'horaire'
        self.fields['horaire'].widget.attrs.update({
            'class': 'form-control',
            'id': 'horaire',
            'required': True
        })

        # Horaire
        preference_employer_disponibles = Utilisateur.objects.filter(is_active=True, roles__role='EMPLOYER')

        # Récupérer les horaires déjà sélectionnés pour ce rendez-vous (si édité)
        preference_employer_selectionne = None
        if self.instance and self.instance.preference_employer:
            preference_employer_selectionne = self.instance.preference_employer

        # Filtrer les heures disponibles en fonction de l'horaire sélectionné (s'il existe)
        preference_employer_disponibles = preference_employer_disponibles.exclude(
            pk=preference_employer_selectionne.pk) if preference_employer_selectionne else preference_employer_disponibles

        # Mettre à jour les choix du champ 'horaire'
        self.fields['preference_employer'].queryset = preference_employer_disponibles

        # Mettre à jour les attributs du widget pour le champ 'horaire'
        self.fields['preference_employer'].widget.attrs.update({
            'class': 'form-control',
            'id': 'horaire',
            'required': False
        })


class ChangerMotDePasse(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'style': "color: black;",
            'id': "password",
            'placeholder': "Password",
        })
        self.fields['new_password2'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'style': "color: black;",
            'id': "password",
            'placeholder': "Confirme Password",
        })

    class Meta:
        model = Utilisateur
        fields = ['new_password1', 'new_password2']


class PasswordResetForme(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'type': "email",
            'class': "form-control",
            'style': "color: black;",
            'id': "email",
            'placeholder': "name@example.com",
            'required': '',
            'pattern': '[^ @]*@[^ @]*',
            'name': 'email',
        })


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Rendez_vous
        fields = ['evaluation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluation'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'style': "color: black;",
            'id': "evaluation",
            'required': True,
            'name': 'contact',
        })
