from django.urls import path

app_name = 'admins'
urlpatterns = [
    path('Inscription/', inscription_D, name='inscription_D'),
]