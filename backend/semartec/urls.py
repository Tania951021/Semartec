from django.urls import path
from .views import inicio, contacto

urlpatterns = [
    path('', inicio),
    path('api/contacto/', contacto),
]