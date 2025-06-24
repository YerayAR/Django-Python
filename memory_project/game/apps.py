"""Application configuration for the game app."""

from django.apps import AppConfig


class GameConfig(AppConfig):
    """Django configuration for the ``game`` application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'
