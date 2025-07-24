"""Enrutamiento de URLs para la aplicación del juego."""

from django.urls import path
from ..controllers import views

urlpatterns = [
    # Página principal con el tablero
    path('', views.index, name='index'),
    # EndPoint AJAX para voltear una carta
    path('flip/<int:index>/', views.flip_card, name='flip'),
    # EndPoint para resolver mismatch después de delay
    path('resolve-mismatch/', views.resolve_mismatch, name='resolve_mismatch'),
    # Reinicia la partida actual
    path('restart/', views.restart_game, name='restart'),
    # Iniciar fase de memorización
    path('start-memorizing/', views.start_memorizing, name='start_memorizing'),
    # Iniciar fase de juego
    path('start-playing/', views.start_playing, name='start_playing'),
]
