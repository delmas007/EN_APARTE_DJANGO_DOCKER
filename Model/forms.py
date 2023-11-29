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


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = Rendez_vous
        fields = ['date_rendez_vous', 'heure_rendez_vous', 'type_massage']

    # Vous pouvez ajouter des widgets ou des validations personnalisées ici si nécessaire
    widgets = {
        'date_rendez_vous': forms.DateInput(
            attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'date', 'name': 'date',
                   'required': ''}),
        'heure_rendez_vous': forms.Select(attrs={'class': 'form-control', 'id': 'time', 'name': 'time'}),
        'type_massage': forms.ChoiceField(
            choices=Rendez_vous.TYPE_MASSAGE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'reason', 'required': True}),
        )
    }
