from django.urls import path

from Model.views import Connexion, inscription, Rendez_vouss, Deconnexion, activate, passwordResetConfirm, \
    password_reset_request, evaluations, evaluation_email

app_name = 'Model'

urlpatterns = [
    path('Connexion/', Connexion.as_view(), name='connexion'),
    path('Deconnexion/', Deconnexion.as_view(), name='Deconnexion'),
    path('Inscription/', inscription, name='inscription'),
    path('Rendez_vous/', Rendez_vouss, name='Rendez_vous'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    # path("password_change", password_change, name="password_change"),
    path("password_reset", password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', passwordResetConfirm, name='réinitialisation'),
    path('evaluation/<uidb64>/<token>', evaluations, name='evaluation'),
    path("mail_eva", evaluation_email, name="mail_evaluation"),

]
