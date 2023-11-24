from django.urls import path
from .views import form_handler, raise_error_frequent_call


app_name = 'requestdataappp'
urlpatterns = [
    path('form/', form_handler, name='form_handler'),
]
