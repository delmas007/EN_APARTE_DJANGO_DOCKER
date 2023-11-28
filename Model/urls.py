from django.urls import path

from Model.views import Connexion, inscription

app_name = 'Model'

urlpatterns = [
    path('Connexion/', Connexion.as_view(), name='connexion'),
    path('Inscription/', inscription, name='inscription'),
]
