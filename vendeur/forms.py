from django.contrib.auth.forms import UserCreationForm

from Model.models import Produit


class UserRegistrationFormee(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "nom",
            'placeholder': "Nom",
            'required': True,
            'name': 'nom',
        })
        self.fields['description'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "prenom",
            'placeholder': "prenom",
            'required': '',
            'name': 'prenom',
        })
        self.fields['prix'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "contact",
            'placeholder': "10000",
            'required': True,
            'name': 'contact',
        })
        self.fields['promotion'].widget.attrs.update({
            'type': "text",
            'class': "form-control",
            'id': "commune",
            'placeholder': "abidjan",
            'required': '',
            'name': 'commune',
        })
        self.fields['pourcentage_promotion'].widget.attrs.update({
            'type': "checkbox",
            'name': "pourcentage",
            'class': "form-check-input",
            'id': "pourcentage",
            'role': "switch"
        })
        self.fields['image'].widget.attrs.update({
            'type': "file",
            'class': "custom-file-input",
            'id': "image",
        })

    class Meta:
        model = Produit
        fields = ('nom', 'description', 'prix', 'promotion', 'pourcentage_promotion', 'image')
