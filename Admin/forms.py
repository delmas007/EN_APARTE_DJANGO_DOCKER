from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from Model.models import Utilisateur, Rendez_vous, Service


class UserRegistrationForme(UserCreationForm):
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
            'id': "nom",
            'placeholder': "Nom",
            'required': True,
            'name': 'nom',
        })
        self.fields['prenom'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "prenom",
            'placeholder': "prenom",
            'required': '',
            'name': 'prenom',
        })
        self.fields['contact'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "contact",
            'placeholder': "0715226698",
            'required': True,
            'name': 'contact',
        })
        self.fields['commune'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "commune",
            'placeholder': "abidjan",
            'required': '',
            'name': 'commune',
        })
        self.fields['sexe'].widget.attrs.update({
            'name': "sexe",
            'style': "color: #212529;width: 100%;",
            'class': "form-control select2",
            'id': "sexe",
        })
        self.fields['roles'].widget.attrs.update({
            'name': "roles",
            'style': "color: #212529;width: 100%;",
            'class': "form-control",
            'id': "roles",
        })
        self.fields['password1'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'id': "password",
            'placeholder': "Password",
        })
        self.fields['password2'].widget.attrs.update({
            'type': "password",
            'name': 'password',
            'class': "form-control ",
            'id': "password",
            'placeholder': "Confirme Password",
        })

    class Meta:
        model = Utilisateur
        fields = ('email', 'nom', 'prenom', 'contact', 'commune', 'sexe', 'roles')


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'style': "color: black;",
            'id': "type",
            'name': 'type',
        })
        self.fields['description'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "description",
            'name': 'description',
        })
        self.fields['prix'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "prix",
            'required': True,
            'name': 'prix',
        })

    class Meta:
        model = Service
        fields = ['type', 'description', 'prix']
