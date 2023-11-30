from django import forms


class ConfirmationReservationForm(forms.Form):
    reservation_id = forms.IntegerField(widget=forms.HiddenInput())
    confirmation = forms.BooleanField(widget=forms.HiddenInput())
