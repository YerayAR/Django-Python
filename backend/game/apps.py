"""Configuración de la aplicación ``game``."""

from django.apps import AppConfig


class GameConfig(AppConfig):
    """Configura la aplicación ``game`` dentro del proyecto."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'
