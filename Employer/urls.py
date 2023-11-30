from django.urls import path

from Employer.views import  reservations_en_attente

app_name = 'employer'

urlpatterns = [

    path('reservation/', reservations_en_attente, name='reservation'),
]