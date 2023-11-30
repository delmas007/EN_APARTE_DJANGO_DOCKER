from django.urls import path

from Employer.views import EmployerConfirme

app_name = 'employer'

urlpatterns = [

    path('reservation/', EmployerConfirme, name='reservation'),
]