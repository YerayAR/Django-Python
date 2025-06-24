import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .logic import GameBoard

SESSION_KEY = 'game_state'


def get_game(request):
    data = request.session.get(SESSION_KEY)
    game = GameBoard(data)
    request.session[SESSION_KEY] = game.to_dict()
    return game


def index(request):
    game = get_game(request)
    context = {
        'game': game,
    }
    return render(request, 'index.html', context)


def flip_card(request, index):
    game = get_game(request)
    mismatch = False
    if index == -1:
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
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
    return redirect(reverse('index'))


def start_memorizing(request):
    """Start the memorizing phase"""
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
    """Start the playing phase"""
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
