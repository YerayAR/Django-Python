"""Unit and view tests for the Memory Game application."""

from django.test import Client, TestCase, SimpleTestCase
from django.urls import reverse

from .logic import GameBoard


class GameBoardTests(SimpleTestCase):
    """Tests for the :class:`GameBoard` logic class."""

    def setUp(self):
        self.board = GameBoard()

    def _pair_indices(self):
        """Return the first pair of matching card indices."""
        value = self.board.cards[0]
        other = self.board.cards.index(value, 1)
        return 0, other

    def _mismatched_indices(self):
        """Return two indices that do not contain the same card value."""
        first = 0
        second = next(i for i, v in enumerate(self.board.cards) if v != self.board.cards[first])
        return first, second

    def test_initial_board_setup(self):
        self.assertEqual(len(self.board.cards), 16)
        self.assertEqual(len(self.board.states), 16)
        self.assertTrue(all(s == 0 for s in self.board.states))
        self.assertEqual(self.board.moves, 0)
        self.assertEqual(self.board.phase, 'setup')

    def test_flip_valid_card(self):
        self.board.start_playing()
        mismatch = self.board.flip(0)
        self.assertFalse(mismatch)
        self.assertEqual(self.board.states[0], 1)
        self.assertEqual(self.board.moves, 0)

    def test_matching_cards_become_paired(self):
        self.board.start_playing()
        i, j = self._pair_indices()
        self.board.flip(i)
        mismatch = self.board.flip(j)
        self.assertFalse(mismatch)
        self.assertEqual(self.board.states[i], 2)
        self.assertEqual(self.board.states[j], 2)
        self.assertEqual(self.board.moves, 1)

    def test_non_matching_cards_hide_again(self):
        self.board.start_playing()
        i, j = self._mismatched_indices()
        self.board.flip(i)
        mismatch = self.board.flip(j)
        self.assertTrue(mismatch)
        # resolve mismatch
        self.board.flip(None)
        self.assertEqual(self.board.states[i], 0)
        self.assertEqual(self.board.states[j], 0)
        self.assertEqual(self.board.moves, 1)

    def test_new_game_resets_board(self):
        self.board.start_playing()
        self.board.flip(0)
        self.board.new_game()
        self.assertEqual(self.board.phase, 'setup')
        self.assertEqual(self.board.moves, 0)
        self.assertTrue(all(s == 0 for s in self.board.states))

    def test_move_counter_increments(self):
        self.board.start_playing()
        i, j = self._mismatched_indices()
        self.board.flip(i)
        self.board.flip(j)
        self.assertEqual(self.board.moves, 1)
        self.board.flip(None)
        a, b = self._pair_indices()
        self.board.flip(a)
        self.board.flip(b)
        self.assertEqual(self.board.moves, 2)

    def test_victory_condition(self):
        self.board.start_playing()
        values_done = set()
        for idx, value in enumerate(self.board.cards):
            if value in values_done:
                continue
            first = idx
            second = self.board.cards.index(value, idx + 1)
            self.board.flip(first)
            self.board.flip(second)
            values_done.add(value)
        self.assertTrue(self.board.is_win())
        self.assertEqual(self.board.moves, 8)

    def test_invalid_index_ignored(self):
        self.board.start_playing()
        mismatch = self.board.flip(-1)
        self.assertFalse(mismatch)
        mismatch = self.board.flip(100)
        self.assertFalse(mismatch)
        self.assertEqual(self.board.moves, 0)
        self.assertTrue(all(s == 0 for s in self.board.states))

    def test_third_flip_not_allowed(self):
        self.board.start_playing()
        i, j = self._mismatched_indices()
        self.board.flip(i)
        self.board.flip(j)
        k = next(x for x in range(len(self.board.cards)) if x not in (i, j))
        mismatch = self.board.flip(k)
        self.assertFalse(mismatch)
        self.assertEqual(self.board.states[k], 0)
        self.assertEqual(self.board.moves, 1)


class ViewTests(TestCase):
    """Tests for Django views in ``game.views``."""

    def setUp(self):
        self.client = Client()

    def test_index_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('game_state', self.client.session)

    def test_restart_resets_board(self):
        self.client.get(reverse('index'))
        self.client.get(reverse('flip', args=[0]))
        before = self.client.session['game_state']
        self.assertNotEqual(before['moves'], 0 or before['states'][0])
        self.client.get(reverse('restart'))
        after = self.client.session['game_state']
        self.assertEqual(after['moves'], 0)
        self.assertTrue(all(s == 0 for s in after['states']))

    def test_flip_endpoint_valid(self):
        self.client.get(reverse('index'))
        response = self.client.get(reverse('flip', args=[0]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['states'][0], 1)
        self.assertEqual(self.client.session['game_state']['states'][0], 1)

    def test_flip_invalid_index(self):
        self.client.get(reverse('index'))
        response = self.client.get(reverse('flip', args=[99]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(all(s == 0 for s in data['states']))

    def test_session_persists_between_requests(self):
        self.client.get(reverse('index'))
        self.client.get(reverse('flip', args=[0]))
        state_after_flip = self.client.session['game_state']['states'][0]
        self.client.get(reverse('index'))
        state_after_reload = self.client.session['game_state']['states'][0]
        self.assertEqual(state_after_reload, state_after_flip)

    def test_start_memorizing_view(self):
        self.client.get(reverse('index'))
        response = self.client.get(reverse('start_memorizing'))
        data = response.json()
        self.assertEqual(data['phase'], 'memorizing')
        self.assertTrue(all(s == 1 for s in data['states']))
        self.assertEqual(self.client.session['game_state']['phase'], 'memorizing')

    def test_start_playing_view(self):
        self.client.get(reverse('index'))
        self.client.get(reverse('start_memorizing'))
        response = self.client.get(reverse('start_playing'))
        data = response.json()
        self.assertEqual(data['phase'], 'playing')
        self.assertTrue(all(s == 0 for s in data['states']))
        self.assertEqual(self.client.session['game_state']['phase'], 'playing')

    def test_prevent_third_flip_server_side(self):
        self.client.get(reverse('index'))
        self.client.get(reverse('start_playing'))
        self.client.get(reverse('flip', args=[0]))
        self.client.get(reverse('flip', args=[1]))
        response = self.client.get(reverse('flip', args=[2]))
        data = response.json()
        self.assertEqual(self.client.session['game_state']['states'][2], 0)
        self.assertEqual(data['moves'], 1)

