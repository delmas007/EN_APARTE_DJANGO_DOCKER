from django.urls import path

from Model.views import Connexion, inscription, Rendez_vous, Deconnexion, activate, passwordResetConfirm, \
    password_reset_request

app_name = 'Model'

urlpatterns = [
    path('Connexion/', Connexion.as_view(), name='connexion'),
    path('Deconnexion/', Deconnexion.as_view(), name='Deconnexion'),
    path('Inscription/', inscription, name='inscription'),
    path('Rendez_vous/', Rendez_vous, name='Rendez_vous'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    # path("password_change", password_change, name="password_change"),
    path("password_reset", password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', passwordResetConfirm, name='réinitialisation'),
]
