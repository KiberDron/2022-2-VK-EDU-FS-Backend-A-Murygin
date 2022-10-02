import unittest
from homework1 import TicTacGame


class TestTicTacGame(unittest.TestCase):

    def test_check_winner(self):
        game = TicTacGame()
        self.assertTrue(game.check_winner('X', {'X': [7, 4, 1], 'O': [9, 5]}))
        self.assertTrue(game.check_winner('X', {'X': [1, 2, 5, 3], 'O': [6, 7, 8]}))
        self.assertTrue(game.check_winner('X', {'X': [1, 9, 3, 5], 'O': [6, 7, 3]}))
        self.assertTrue(game.check_winner('X', {'X': [8, 5, 1, 4, 9], 'O': [3, 6, 2, 7]}))
        self.assertTrue(game.check_winner('O', {'X': [7, 4, 2], 'O': [6, 9, 3]}))
        self.assertTrue(game.check_winner('O', {'X': [9, 8, 4], 'O': [3, 5, 7]}))
        self.assertTrue(game.check_winner('O', {'X': [4, 7, 6, 9], 'O': [1, 2, 8, 5]}))
        self.assertTrue(game.check_winner('O', {'X': [1, 2, 4, 5], 'O': [7, 8, 9, 6]}))
        self.assertFalse(game.check_winner('X', {'X': [1, 2, 8], 'O': [4, 5]}))
        self.assertFalse(game.check_winner('X', {'X': [1, 2, 4, 5], 'O': [6, 7, 8]}))
        self.assertFalse(game.check_winner('X', {'X': [2, 3, 5, 6], 'O': [4, 8, 7]}))
        self.assertFalse(game.check_winner('X', {'X': [2, 5, 7, 9, 4], 'O': [1, 6, 8, 3]}))
        self.assertFalse(game.check_winner('O', {'X': [1, 2, 4], 'O': [3, 6, 8]}))
        self.assertFalse(game.check_winner('O', {'X': [7, 8, 6], 'O': [1, 2, 9]}))
        self.assertFalse(game.check_winner('O', {'X': [1, 3, 4, 6], 'O': [2, 5, 7, 9]}))
        self.assertFalse(game.check_winner('O', {'X': [3, 6, 4, 7], 'O': [1, 2, 8, 9]}))

    def test_check_draw(self):
        game = TicTacGame()
        self.assertTrue(game.check_draw({'X': [2, 5, 7, 9, 4], 'O': [1, 6, 8, 3]}))
        self.assertTrue(game.check_draw({'X': [2, 1, 4, 7, 8], 'O': [3, 5, 6, 9]}))
        self.assertTrue(game.check_draw({'X': [2, 3, 6, 9, 8], 'O': [1, 4, 5, 7]}))
        self.assertTrue(game.check_draw({'X': [4, 7, 8, 9, 6], 'O': [1, 2, 3, 5]}))
        self.assertTrue(game.check_draw({'X': [6, 3, 2, 1, 4], 'O': [5, 7, 8, 9]}))
        self.assertFalse(game.check_draw({'X': [1, 5], 'O': [6]}))
        self.assertFalse(game.check_draw({'X': [7, 4, 1], 'O': [9, 5]}))
        self.assertFalse(game.check_draw({'X': [2, 5, 6], 'O': [1, 4, 7]}))
        self.assertFalse(game.check_draw({'X': [1, 2, 4, 3], 'O': [7, 8, 6]}))
        self.assertFalse(game.check_draw({'X': [4, 5, 8, 9], 'O': [1, 2, 7]}))


if __name__ == '__main__':
    unittest.main()
