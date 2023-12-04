from django.urls import path

from Employer.views import reservations_en_attente, reservations_confirmer, debut_rendez_vous, fin_rendez_vous

app_name = 'employer'

urlpatterns = [

    path('reservation/', reservations_en_attente, name='reservation'),
    path('reservations_confirmer/', reservations_confirmer, name='reservation_confirmer'),
    path('debut_rendez_vous/<int:rendez_vous_id>/', debut_rendez_vous, name='debut_rendez_vous'),
    path('fin_rendez_vous/<int:rendez_vous_id>/', fin_rendez_vous, name='fin_rendez_vous')
]