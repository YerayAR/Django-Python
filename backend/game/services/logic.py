"""Lógica central del juego de memoria."""

import random


class GameBoard:
    """Representa el tablero y su estado actual."""

    def __init__(self, data=None):
        """Crea un tablero nuevo o restaura uno desde ``data``.

        Parameters
        ----------
        data : dict, optional
            Estado serializado previamente devuelto por :meth:`to_dict`.
        """
        if data:
            # Restore saved state from the session
            self.cards = data.get('cards', [])
            self.states = data.get('states', [])
            self.moves = data.get('moves', 0)
            self.phase = data.get('phase', 'setup')  # setup, memorizing, playing
            self.start_time = data.get('start_time', None)
        else:
            self.new_game()

    def new_game(self):
        """Inicializa un nuevo tablero mezclado en fase ``setup``."""
        pairs = list(range(8)) * 2
        random.shuffle(pairs)
        self.cards = pairs
        # 0 = hidden, 1 = flipped, 2 = matched
        self.states = [0] * len(self.cards)
        self.moves = 0
        self.phase = 'setup'  # setup, memorizing, playing
        self.start_time = None

    def flip(self, index):
        """Voltea una carta y evalúa si se ha encontrado una pareja.

        Parameters
        ----------
        index : int or None
            Index of the card to flip. ``None`` signals that a mismatch should
            be resolved by hiding the previously flipped cards.

        Returns
        -------
        bool
            ``True`` if the flipped pair does not match, ``False`` otherwise.
        """
        if index is None:
            # Called after a delay to hide unmatched cards
            self._resolve_mismatch()
            return False

        # Only allow flipping in playing phase
        if not self.can_flip():
            return False

        if index < 0 or index >= len(self.cards):
            return False

        if self.states[index] != 0:
            return False

        if len(self._uncovered_indices()) == 2:
            return False

        # Reveal the selected card
        self.states[index] = 1
        mismatch = False
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            if self.cards[i] == self.cards[j]:
                self.states[i] = self.states[j] = 2
                mismatch = False
            else:
                mismatch = True
            self.moves += 1
        return mismatch

    def _resolve_mismatch(self):
        """Oculta las dos cartas volteadas si no coinciden."""
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            if self.cards[i] != self.cards[j]:
                self.states[i] = self.states[j] = 0

    def _uncovered_indices(self):
        """Devuelve los índices de cartas volteadas que aún no se han emparejado."""
        return [i for i, s in enumerate(self.states) if s == 1]

    def is_win(self):
        """Indica si todas las cartas han sido emparejadas."""
        return all(s == 2 for s in self.states)
    
    def start_memorizing(self):
        """Inicia la fase de memorización mostrando todas las cartas."""
        self.phase = 'memorizing'
        import time
        self.start_time = time.time()
    
    def start_playing(self):
        """Comienza la fase de juego ocultando las cartas y reiniciando movimientos."""
        self.phase = 'playing'
        # Reset all cards to hidden state
        self.states = [0] * len(self.cards)
        self.moves = 0
    
    def can_flip(self):
        """Devuelve ``True`` si se pueden voltear cartas en la fase actual."""
        return self.phase == 'playing'

    def to_dict(self):
        """Serializa el tablero a un diccionario para almacenarlo en sesión."""
        return {
            'cards': self.cards,
            'states': self.states,
            'moves': self.moves,
            'phase': self.phase,
            'start_time': self.start_time,
        }
