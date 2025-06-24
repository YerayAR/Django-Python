import random


class GameBoard:
    def __init__(self, data=None):
        if data:
            self.cards = data.get('cards', [])
            self.states = data.get('states', [])
            self.moves = data.get('moves', 0)
        else:
            self.new_game()

    def new_game(self):
        pairs = list(range(8)) * 2
        random.shuffle(pairs)
        self.cards = pairs
        self.states = [0] * len(self.cards)
        self.moves = 0

    def flip(self, index):
        if index is None:
            self._resolve_mismatch()
            return False

        if index < 0 or index >= len(self.cards):
            return False

        if self.states[index] != 0:
            return False

        if len(self._uncovered_indices()) == 2:
            return False

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
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            if self.cards[i] != self.cards[j]:
                self.states[i] = self.states[j] = 0

    def _uncovered_indices(self):
        return [i for i, s in enumerate(self.states) if s == 1]

    def is_win(self):
        return all(s == 2 for s in self.states)

    def to_dict(self):
        return {
            'cards': self.cards,
            'states': self.states,
            'moves': self.moves,
        }
