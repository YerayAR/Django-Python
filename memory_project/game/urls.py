from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flip/<int:index>/', views.flip_card, name='flip'),
    path('restart/', views.restart_game, name='restart'),
    path('start-memorizing/', views.start_memorizing, name='start_memorizing'),
    path('start-playing/', views.start_playing, name='start_playing'),
]
