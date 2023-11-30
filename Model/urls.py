from django.urls import path

from Model.views import Connexion, inscription, Rendez_vous, Deconnexion

app_name = 'Model'

urlpatterns = [
    path('Connexion/', Connexion.as_view(), name='connexion'),
    path('Deconnexion/', Deconnexion.as_view(), name='Deconnexion'),
    path('Inscription/', inscription, name='inscription'),
    path('Rendez_vous/', Rendez_vous, name='Rendez_vous'),
]
