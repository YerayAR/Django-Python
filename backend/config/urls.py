"""Configuración de rutas a nivel de proyecto."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Administración de Django
    path('admin/', admin.site.urls),
    # Rutas principales de la aplicación
    path('', include('game.routes.urls')),
]
