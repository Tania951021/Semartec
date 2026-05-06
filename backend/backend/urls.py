from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ← ESTA LÍNEA FALTA
    path('', include('semartec.urls')),
]