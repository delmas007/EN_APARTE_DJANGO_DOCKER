from django.contrib.auth.forms import AuthenticationForm


class ConnexionForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'type':"email",
            'class':"form-control",
            'style':"color: black;",
            'id':"email",
            'placeholder':"name@example.com",
            'required':'',
            'pattern':'[^ @]*@[^ @]*',
            'name':'email',
        })
        self.fields['password'].widget.attrs.update({
            'type':"password",
            'name':'password',
            'class':"form-control ",
            'style':"color: black;",
            'id':"password",
            'placeholder':"Password",
        })