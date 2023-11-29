from django.urls import path

from Vitrine.views import Accueil, Contact, Faq

app_name = 'vitrine'

urlpatterns = [

    path('Contact/', Contact, name='Contact'),
    path('Faq/', Faq, name='Faq'),
]
