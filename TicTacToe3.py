from typing import List
import copy
from random import randint


class Cell:
    state: str = ' '

    def is_free(self):
        return self.state == ' '

    def set_state(self, state: str):
        self.state = state

    def get_state(self):
        return self.state

    def __repr__(self) -> str:
        return self.state


class Board:
    size: int = 0
    board: List[List[Cell]] = []

    def __init__(self, size, win_line_size):
        self.size = size
        self.win_line_size = win_line_size
        tmp_line = []
        for i in range(size):
            tmp_line.append(Cell())
        self.board = [copy.deepcopy(tmp_line) for i in range(size)]

    def is_free(self, x: int, y: int) -> bool:
        return self.board[x][y].is_free()

    def set_symbol(self, x: int, y: int, symbol: str) -> None:
        self.board[x][y].set_state(symbol)

    def get_symbol(self, x: int, y: int) -> str:
        return self.board[x][y].get_state()

    def is_full(self):
        count = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.is_free(x, y):
                    count += 1
        if count == 0:
            return 'Ничья'
        return False


class GameBoard(Board):
    def print_board(self):
        for i in range(self.size):
            print('-' * (self.size * 3 + (self.size +1)))
            for j in range(self.size):
                print('|', self.board[i][j], end = ' ')
            print('|')
        print('-' * (self.size * 3 + (self.size + 1)))

    def check_win_for_symbol_in_row_and_col(self, board, symbol):
        new_mas = copy.deepcopy(board)
        new_mas.sort()
        for i in range(len(new_mas)):
            new_mas[i][1] -= i
        for j in range(len(new_mas)):
            if new_mas.count(new_mas[j]) >= self.win_line_size:
                return symbol
        return False

    def check_win_for_symbol_in_diagonal(self, board, symbol):
        diagonal1 = copy.deepcopy(board)
        diagonal2 = copy.deepcopy(board)
        for i in range(len(board)):
            diagonal1[i][1] = board[i][0] + board[i][1] #Преобразование координат, матрица поворота на 45 градусов
            diagonal1[i][0] = board[i][1] - board[i][0]
        diagonal1.sort()
        for i in range(len(diagonal1)):
            diagonal1[i][1] -= i * 2
        for j in range(len(diagonal1)):
            if diagonal1.count(diagonal1[j]) >= self.win_line_size:
                return symbol
        for i in range(len(board)):
            diagonal2[i][0] = board[i][0] + board[i][1]
            diagonal2[i][1] = board[i][1] - board[i][0]
        diagonal2.sort()
        for i in range(len(diagonal2)):
            diagonal2[i][1] -= i * 2
        for j in range(len(diagonal2)):
            if diagonal2.count(diagonal2[j]) >= self.win_line_size:
                return symbol
        return False

    def is_win(self, symbol):
        r_mas = []
        c_mas = []
        for row in range(self.size):
            for col in range(self.size):
                if self.get_symbol(row, col) == symbol:
                    r_mas += [[row, col]]
                    c_mas += [[col, row]]
        if self.check_win_for_symbol_in_row_and_col(r_mas, symbol):
            return symbol
        elif self.check_win_for_symbol_in_row_and_col(c_mas, symbol):
            return symbol
        elif self.check_win_for_symbol_in_diagonal(r_mas, symbol):
            return symbol

        return False

class Player:
    def __init__(self, symbol, board: Board):
        self._symbol = symbol
        self._board = board

    def get_symbol(self):
        return self._symbol
    
    
class AiPlayer(Player):
    def min_max(self, board: GameBoard, depth, is_maximum: bool) -> int:
        if self._symbol == 'x':
            ai_symbol = 'x'
            human_symbol = 'o'
        else:
            ai_symbol = 'o'
            human_symbol = 'x'
        if board.is_win(ai_symbol):
            return 5
        if board.is_win(human_symbol):
            return -5
        if not board.is_win(ai_symbol) and not board.is_win(human_symbol):
            return 0

        if is_maximum:
            best_score = - sys.maxsize
            for i in range(self._board.size):
                for j in range(self._board.size):
                    if board.is_free(i, j):
                        board.set_symbol(i, j, ai_symbol)
                        score = self.min_max(board, depth+1, False)
                        board.set_symbol(i, j, ' ')
                        best_score = max(best_score, score)
        else:
            best_score = sys.maxsize
            for i in range(self._board.size):
                for j in range(self._board.size):
                    if board.is_free(i, j):
                        board.set_symbol(i, j, human_symbol)
                        score = self.min_max(board, depth + 1, True)
                        board.set_symbol(i, j, ' ')
                        best_score = min(best_score, score)

        return best_score


    def make_turn(self):
        if self._board.is_free(self._board.size // 2, self._board.size // 2):
            self._board.set_symbol(self._board.size // 2, self._board.size // 2, self._symbol)
            print('Поставлен символ', self._symbol, ', координаты', 1, 1)
        else:
            best_score = - sys.maxsize
            field = copy.deepcopy(self._board)
            for i in range(self._board.size):
                for j in range(self._board.size):
                    if field.is_free(i,j):
                        field.set_symbol(i, j, self._symbol)
                        score = self.min_max(field, 0, False)
                        field.set_symbol(i, j, ' ')
                        if score > best_score:
                            best_score = score
                            x = i
                            y = j
            self._board.set_symbol(x, y, self._symbol)
            print('Поставлен символ', self._symbol, ', координаты', x, y)

    
class RandomPlayer(Player):
    def make_turn(self):
         x, y = randint(0, self._board.size - 1), randint(0, self._board.size- 1)
         while not self._board.is_free(x, y):
             x, y = randint(0, self._board.size - 1), randint(0, self._board.size - 1)
         self._board.set_symbol(x, y, self._symbol)
         print('Поставлен символ', self._symbol, ', координаты', x, y)

class HumanPlayer(Player):

    def make_turn(self):
        print('Ход символа', self._symbol, end=' ')
        x, y = input('введите 2 числа через пробел: ').split()
        x, y = int(x), int(y)
        a = [i for i in range(self._board.size)]
        while not (x in a and y in a):
            print('Введите валидные координаты через пробел: ')
            x, y = input('введите 2 числа через пробел: ').split()
            x, y = int(x), int(y)
        while not self._board.is_free(x, y):
            print('Клетка занята')
            x, y = input('введите 2 числа через пробел: ').split()
            x, y = int(x), int(y)
        self._board.set_symbol(x, y, self._symbol)


class Game:
    players: List[Player] = []

    def add_player(self, player):
        self.players.append(player)

    def play(self):
        symbols = 'xo+#@-=&*%'
        size = int(input('Размер поля: '))
        win_line_size = int(input('Длина линии: '))
        game_board = GameBoard(size, win_line_size)
        count_players = int(input('Количество игроков (от 2 до 10): '))
                if count_players == 2:
            a = input("Вы будете играть с компьютером? Введите y или n: ")
            if a == 'y':
                n = input("Вы будете ходить первым? Введите y или n: ")
                if n == 'y':
                    p1 = HumanPlayer(symbols[0], game_board)
                    self.add_player(p1)
                    p2 = AiPlayer(symbols[1], game_board)
                    self.add_player(p2)
                else:
                    p1 = AiPlayer(symbols[0], game_board)
                    self.add_player(p1)
                    p2 = HumanPlayer(symbols[1], game_board)
                    self.add_player(p2)
            else:
                p1 = HumanPlayer(symbols[0], game_board)
                self.add_player(p1)
                p2 = HumanPlayer(symbols[1], game_board)
                self.add_player(p2)
        elif 2 < count_players < 10:
            a = int(input("Введите количество игроков-компьютеров: "))
            if a == 0:
                for i in range(count_players):
                    p = HumanPlayer(symbols[i], game_board)
                    self.add_player(p)
            if 0 < a < count_players:
                for i in range(count_players-a):
                    p = HumanPlayer(symbols[i], game_board)
                    self.add_player(p)
                for i in range(1, a+1):
                    p = RandomPlayer(symbols[-i], game_board)
                    self.add_player(p)
            if a == count_players:
                for i in range(count_players):
                    p = RandomPlayer(symbols[i], game_board)
                    self.add_player(p)
      win = False
        while not win:
            for player in self.players:
                game_board.print_board()
                player.make_turn()
                if game_board.is_win(player.get_symbol()):
                    print("Game over! win ", player.get_symbol())
                    win = True
                    break
                if game_board.is_full():
                    print("Piece")
                    win = True
                    break



g = Game()
g.play()
