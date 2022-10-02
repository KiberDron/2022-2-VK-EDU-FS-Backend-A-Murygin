import random
import time


class TicTacGame:

    def show_board(self, board):
        print('___________________')
        print('|     |     |     |')
        print(f'|  {board[0]}  |  {board[1]}  |  {board[2]}  |')
        print('|_____|_____|_____|')
        print('|     |     |     |')
        print(f'|  {board[3]}  |  {board[4]}  |  {board[5]}  |')
        print('|_____|_____|_____|')
        print('|     |     |     |')
        print(f'|  {board[6]}  |  {board[7]}  |  {board[8]}  |')
        print('|_____|_____|_____|')
        print('\n')

    def validate_input(self, side, board) -> int:
        valid = False
        while not valid:
            print(side + ' turn. Choose your square')
            try:
                turn = int(input())
            except ValueError:
                print('Incorrect input. Type number from 1 to 9')
                continue
            if turn < 1 or turn > 9:
                print('Incorrect input. Type number from 1 to 9')
                continue
            if str(board[turn - 1]) in 'XO':
                print('Incorrect input. This square is occupied')
                continue
            valid = True
        board[turn - 1] = side
        return turn

    def start_game(self):
        print('_' * 21)
        print('player vs player game')
        print('_' * 21 + '\n')
        board = list(range(1, 10))
        data = {'X': [], 'O': []}
        side = 'X'
        self.show_board(board)
        board = [' ' for _ in range(9)]
        while True:
            data[side].append(self.validate_input(side, board))
            self.show_board(board)
            if self.check_winner(side, data):
                print(f'The winner is {side}')
                break
            if self.check_draw(data):
                print('The game is draw')
                break
            side = 'O' if side == 'X' else 'X'

    def check_winner(self, side, data) -> bool:
        win_combinations = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7),
                            (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))
        for combination in win_combinations:
            if all(number in data[side] for number in combination):
                return True
        return False

    def check_draw(self, data) -> bool:
        if len(data['X']) + len(data['O']) == 9:
            return True
        else:
            return False

    def computer_input(self, side, board) -> int:
        valid = False
        print(side + ' turn')
        while not valid:
            turn = random.randint(1, 9)
            if str(board[turn - 1]) in 'XO':
                continue
            valid = True
        board[turn - 1] = side
        return turn

    def computer_game(self):
        print('_' * 25)
        print('computer vs computer game')
        print('_' * 25 + '\n')
        board = [' ' for _ in range(9)]
        data = {'X': [], 'O': []}
        side = 'X'
        while True:
            data[side].append(self.computer_input(side, board))
            time.sleep(3)
            self.show_board(board)
            if self.check_winner(side, data):
                print(f'The winner is {side}')
                break
            if self.check_draw(data):
                print('The game is draw')
                break
            side = 'O' if side == 'X' else 'X'


game = TicTacGame()
game.start_game()  # run for player vs player game
# game.computer_game()  # run for computer vs computer game
