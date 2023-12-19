from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from Model.models import Utilisateur, Rendez_vous


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
        fields = ['date_rendez_vous', 'service', 'horaire']

        widgets = {
            'date_rendez_vous': XYZ_DateInput(attrs={
                'id': 'id_date_rendez_vous',  # Utilisez l'ID généré par Django
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].widget.attrs.update({
            'name': 'reason',
            'class': 'form-control',
            'id': 'service',  # Utilisez l'ID généré par Django
            'required': True
        })
        self.fields['horaire'].widget.attrs.update({
            'name': 'reason',
            'class': 'form-control',
            'id': 'horaire',  # Utilisez l'ID généré par Django
            'required': True
        })
