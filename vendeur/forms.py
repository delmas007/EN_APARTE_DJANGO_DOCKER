from django import forms


from Model.models import Produi


class UserRegistrationFormee(forms.ModelForm):
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
            'id': "description",
            'placeholder': "description",
            'required': True,
            'name': 'description',
        })
        self.fields['prix'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "prix",
            'placeholder': "10000",
            'required': True,
            'name': 'prix',
        })
        self.fields['pourcentage_promotion'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "pourcentage_promotion",
            'placeholder': "10",
            'name': 'pourcentage_promotion',
        })
        self.fields['promotion'].widget.attrs.update({
            'type': "checkbox",
            'class': "form-check-input ",
            'id': "exampleCheck1",
        })
        self.fields['image'].widget.attrs.update({
            'type': "file",
            'class': "custom-file-input",
            'id': "image",
            'required': True,
        })

    class Meta:
        model = Produit
        fields = ('nom', 'description', 'prix', 'promotion', 'pourcentage_promotion', 'image')


class UserRegistrationFor(forms.ModelForm):
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
            'id': "description",
            'placeholder': "description",
            'required': True,
            'name': 'description',
        })
        self.fields['prix'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "prix",
            'placeholder': "10000",
            'required': True,
            'name': 'prix',
        })
        self.fields['pourcentage_promotion'].widget.attrs.update({
            'type': "number",
            'class': "form-control",
            'id': "pourcentage_promotion",
            'placeholder': "10",
            'name': 'pourcentage_promotion',
        })
        self.fields['promotion'].widget.attrs.update({
            'type': "checkbox",
            'class': "form-check-input ",
            'id': "exampleCheck1",
        })

    class Meta:
        model = Produit
        fields = ('nom', 'description', 'prix', 'promotion', 'pourcentage_promotion', 'image')
