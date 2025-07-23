"""Vistas de Django para la aplicación Memory Game."""

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from ..services.logic import GameBoard

# Clave empleada para almacenar el :class:`GameBoard` serializado en la sesión
SESSION_KEY = 'game_state'


def get_game(request):
    """Obtiene el :class:`GameBoard` actual desde la sesión.

    Si no existe un juego en la sesión se crea uno nuevo y se persiste
    nuevamente en la sesión para mantener el estado entre peticiones.

    Parameters
    ----------
    request : HttpRequest
        Solicitud HTTP que contiene la sesión.

    Returns
    -------
    GameBoard
        Tablero que representa el estado actual del juego.
    """
    data = request.session.get(SESSION_KEY)
    game = GameBoard(data)
    # Persist the (possibly new) game state in the session
    request.session[SESSION_KEY] = game.to_dict()
    return game


def index(request):
    """Renderiza la página principal con el estado actual del tablero."""
    game = get_game(request)
    context = {
        'game': game,
    }
    return render(request, 'index.html', context)


def flip_card(request, index):
    """Voltea la carta indicada por ``index`` y devuelve el estado actualizado."""
    game = get_game(request)
    mismatch = False
    if index == -1:
        # ``-1`` is used by the frontend to resolve a mismatch after a delay
        game.flip(None)
    else:
        mismatch = game.flip(index)

    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': game.states,
        'moves': game.moves,
        'win': game.is_win(),
        'mismatch': mismatch,
        'phase': game.phase,
    }
    return JsonResponse(response)


def restart_game(request):
    """Elimina el juego actual de la sesión y redirige a ``index``."""
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
    return redirect(reverse('index'))


def start_memorizing(request):
    """Pasa el juego a la fase de memorización."""
    game = get_game(request)
    game.start_memorizing()
    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': [1] * len(game.cards),  # Show all cards
        'moves': game.moves,
        'phase': game.phase,
        'win': False,
    }
    return JsonResponse(response)


def start_playing(request):
    """Inicia la fase de juego ocultando las cartas."""
    game = get_game(request)
    game.start_playing()
    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': game.states,
        'moves': game.moves,
        'phase': game.phase,
        'win': False,
    }
    return JsonResponse(response)
