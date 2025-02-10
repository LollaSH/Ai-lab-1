from tkinter import Tk, Canvas, N, W, E, S
import numpy as np
import time
from sys import argv

class Graphics:
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg="green")
        self.root.geometry("800x800")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.bind('<Destroy>', self.destroy)

        self.canvas = Canvas(self.root, bg="green")
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Configure>', self.save_wh)

        self.w = 0
        self.h = 0

        # Allows for players to register callbacks for when a click happens
        self.click_callbacks = []

        self.board = np.zeros((8,8), dtype=int)
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[4, 3] = 1
        self.board[3, 4] = 1

        self.running = True
        self.root.update()

    def destroy(self, event):
        self.running = False

    def save_wh(self, event):
        self.w = event.width
        self.h = event.height
        self.draw()

    def update(self):
        self.root.update()

    def register_click_callback(self, callback):
        self.click_callbacks.append(callback)

    def on_click(self, event):
        sq_w = self.w // 8
        sq_h = self.h // 8
        row = event.y // sq_h
        col = event.x // sq_w
        for f in self.click_callbacks:
            f(row, col)

    def draw(self, board = None):

        if board is not None:
            self.board = board
        else:
            board = self.board

        sq_w = self.w // 8
        sq_h = self.h // 8
        cx = sq_w // 2
        cy = sq_h // 2
        r = min(sq_w, sq_h) * 0.4#0.45
        top = cy - r
        left = cx - r
        bottom = cy + r
        right = cx + r
        self.canvas.delete('all')
        for i in range(8):
            self.canvas.create_line(0, i* sq_h, self.w, i*sq_h, width=5)
            self.canvas.create_line(i*sq_w, 0, i*sq_w, self.h, width=5)

        for i in range(8):
            for j in range(8):
                val = board[i, j]
                if val == 1:
                    self.canvas.create_oval(j*sq_w + left, i*sq_h + top, j*sq_w + right, i*sq_h + bottom, width=5, fill="black", outline="black")
                elif val == -1:
                    self.canvas.create_oval(j*sq_w + left, i*sq_h + top, j*sq_w + right, i*sq_h + bottom, width=5, fill="white")

        self.root.update()

def has_won(board, player):
    nbrEmpty = np.sum(board == 0)
    posMovesPlayer = len(possible_moves(board, player))
    posMovesOthPlayer = len(possible_moves(board, -player))
    pl = np.sum(board == player)
    minuspl = np.sum(board == -player)
    
    if posMovesPlayer == 0 and posMovesOthPlayer == 0 and pl > minuspl:
        return True
    elif posMovesPlayer == 0 and posMovesOthPlayer == 0 and pl < pl:
        return False
    elif nbrEmpty == 1 and posMovesPlayer == 0 and posMovesOthPlayer == 1:
        temp_move = possible_moves(board, -player)[0]
        temp_board = update_board(board, temp_move)
        pl = np.sum(temp_board == player)
        minuspl = np.sum(temp_board == -player)
        if pl > minuspl:
            return True
        elif minuspl > pl:
            return False
    elif nbrEmpty == 1 and posMovesPlayer == 1 and posMovesOthPlayer == 0:
        temp_move = possible_moves(board, player)[0]
        temp_board = update_board(board, temp_move)
        pl = np.sum(temp_board == player)
        minuspl = np.sum(temp_board == -player)
        if pl > minuspl:
            return True
        elif minuspl > pl:
            return False
    elif nbrEmpty == 1 and posMovesPlayer == 1 and posMovesOthPlayer == 1:
        temp_move = possible_moves(board, -player)[0]
        temp_board = update_board(board, temp_move)
        pl = np.sum(temp_board == player)
        minuspl = np.sum(temp_board == -player)
        if pl > minuspl:
            return True
        elif minuspl > pl:
            return False
    return False



def possible_moves(board, player):
    md = dict()

    directions = [
        (1, 0), (-1, 0),  # Vertical (down, up)
        (0, 1), (0, -1),  # Horizontal (right, left)
        (1, 1), (-1, -1), # Diagonal (bottom-right, top-left)
        (1, -1), (-1, 1)  # Diagonal (bottom-left, top-right)
    ]

    for i in range(8):
        for j in range(8):
            if board[i, j] == player:
                for di, dj in directions:
                    flips = 0
                    flipped = set()
                    x, y = i + di, j + dj

                    while 0 <= x < 8 and 0 <= y < 8:
                        b = board[x, y]
                        if b == -player:
                            flipped.add((x, y))
                            flips += 1
                        elif b == 0 and flips > 0:
                            pos = (x, y)
                            if pos in md:
                                md[pos] = md[pos].union(flipped)
                            else:
                                md[pos] = flipped.copy()
                            break
                        elif b == player or (b == 0 and flips == 0):
                            break

                        x += di
                        y += dj

    moves = [
        {'player': player, 'put': slot, 'flipped': flipped}
        for slot, flipped in md.items()
    ]
    
    moves.sort(key=lambda move: len(move['flipped']), reverse=True)

    return moves


def allowed_moves(board, player):
    md = dict()

    directions = [
        (1, 0), (-1, 0),  # Vertical (down, up)
        (0, 1), (0, -1),  # Horizontal (right, left)
        (1, 1), (-1, -1), # Diagonal (bottom-right, top-left)
        (1, -1), (-1, 1)  # Diagonal (bottom-left, top-right)
    ]

    for i in range(8):
        for j in range(8):
            if board[i, j] == player:
                for di, dj in directions:
                    flips = 0
                    flipped = set()
                    x, y = i + di, j + dj

                    while 0 <= x < 8 and 0 <= y < 8:
                        b = board[x, y]
                        if b == -player:
                            flipped.add((x, y))
                            flips += 1
                        elif b == 0 and flips > 0:
                            pos = (x, y)
                            if pos in md:
                                md[pos] = md[pos].union(flipped)
                            else:
                                md[pos] = flipped.copy()
                            break
                        elif b == player or (b == 0 and flips == 0):
                            break

                        x += di
                        y += dj

    return md


def update_board(board, move):
    board = board.copy()
    player = move['player']
    
    for r, c in move['flipped']:
        board[r, c] = player

    
    row, col = move['put']
    board[row, col] = player

    return board

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.winner = 0
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[4, 3] = 1
        self.board[3, 4] = 1
        #self.board = np.random.choice([-1, 0, 1], (3, 3), replace=True)

    def get_board(self):
        return self.board.copy()

    def get_possible_moves(self, player):
        return possible_moves(self.board, player)

    def game_over(self):
        if np.sum(self.board == 0) == 0 or (len(self.get_possible_moves(player=1)) == 0 and len(self.get_possible_moves(player=-1)) == 0):
            blacks = np.sum(self.board == 1)
            whites = np.sum(self.board == -1)
            if blacks > whites:
                self.winner = 1
            elif whites > blacks:
                self.winner = -1
            else:
                self.winner = 0
            return True
        else:
            return False

    def reset(self):
        self.board[:,:] = 0
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[4, 3] = 1
        self.board[3, 4] = 1
        self.winner = 0

    def make_move(self, move):

        if self.winner != 0:
            raise Exception('This game is already over!')

        player = move['player']
        put_row, put_col = move['put']
        flipped = move['flipped']
        num_pieces = np.sum(self.board == player)

        if self.board[put_row, put_col] != 0:
            raise Exception('Cannot place a piece in a non-empty slot!')

        self.board = update_board(self.board, move=move)



class HumanPlayer:
    def __init__(self, player, ui):
        self.player = player
        self.pos = None
        self.ui = ui
        ui.register_click_callback(self.click_callback)

    def click_callback(self, row, col):
        self.pos = (row, col)

    def get_click(self):
        self.pos = None
        while self.pos is None: self.ui.update()
        return self.pos

    def move(self, env):

        board = env.get_board()
        pieces = set(zip(*np.where(board == self.player)))
        moves = allowed_moves(board=board, player = self.player)
        if len(moves) == 0:
            return

        try:
            move = {
                'player': self.player
            }
            pos = self.get_click()
            while pos not in moves: pos = self.get_click()
            move['put'] = pos
            move['flipped'] = moves[pos]

            env.make_move(move)
        except: pass

class RandomPlayer:
    def __init__(self, player):
        self.player = player

    def move(self, env):
        moves = env.get_possible_moves(self.player)
        if len(moves) == 0:
            return
        move = np.random.choice(moves, 1)[0]
        env.make_move(move)


class EvalAlphaBeta:
    def __init__(self, player, max_depth=4):
        self.player = player
        self.max_depth = max_depth

    def move(self, env):
        board = env.get_board()
        best_score = -np.inf
        posMoves = possible_moves(board, self.player)
        if len(posMoves) == 0: return
        best_move = posMoves[0]
        for move in posMoves:
            score = self.min_player(update_board(board, move), best_score, np.inf, 1)
            if score > best_score:
                best_score = score
                best_move = move
        env.make_move(best_move)

    def min_player(self, board, alpha, beta, depth):
        if has_won(board, self.player): return 64
        elif has_won(board, -self.player): return -64
        elif depth == self.max_depth: return np.sum(board == self.player) - np.sum(board == -self.player)
        score = np.inf
        posMovesMinPl = possible_moves(board, -self.player)
        if len(posMovesMinPl) != 0:
            for move in posMovesMinPl:
                score = min(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
                beta = min(beta, score)
                if score <= alpha: break
            return score
        posMovesPl = possible_moves(board, self.player)
        if len(posMovesPl) != 0:
            score = -np.inf
            for move in posMovesPl:
                score = max(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
                alpha = max(alpha, score)
                if score >= beta: break
            return score
        else: return np.sum(board == self.player) - np.sum(board == -self.player)
            
            

    def max_player(self, board, alpha, beta, depth):
        if has_won(board, self.player): return 64
        elif has_won(board, -self.player): return -64
        elif depth == self.max_depth: return np.sum(board == self.player) - np.sum(board == -self.player)
        score = -np.inf
        posMovesPl = possible_moves(board, self.player)
        if len(posMovesPl) != 0:
            score = -np.inf
            for move in posMovesPl:
                score = max(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
                alpha = max(alpha, score)
                if score >= beta: break
            return score
        posMovesMinPl = possible_moves(board, -self.player)
        if len(posMovesMinPl) != 0:
            for move in posMovesMinPl:
                score = min(score, self.max_player(update_board(board, move), alpha, beta, depth+1))
                beta = min(beta, score)
                if score <= alpha: break
            return score
        else: return np.sum(board == self.player) - np.sum(board == -self.player)


def main():

    n_games = 20

    if len(argv) >= 1:
        try:
            n_games = int(argv[1])
        except: pass

    graphics = Graphics()
    env = Othello()
    #graphics.draw(board = env.get_board())

    n_wins = {
        1: 0,
        -1: 0,
        0: 0
    }
    
    #player1 = HumanPlayer(1, graphics)
    #player1 = RandomPlayer(1)
    player1 = EvalAlphaBeta(1)

    #player2 = HumanPlayer(-1, graphics)
    player2 = RandomPlayer(-1)
    #player2 = EvalAlphaBeta(-1)

    n_played = 0
    for _ in range(n_games):
        env.reset()
        graphics.draw(env.board)
        while True:
            time.sleep(0)
            player1.move(env)
            if not graphics.running: break
            graphics.draw(env.board)
            if env.game_over(): break
            time.sleep(0)
            player2.move(env)
            if not graphics.running: break
            graphics.draw(env.board)
            if env.game_over(): break

        if isinstance(player1, HumanPlayer) or isinstance(player2, HumanPlayer):
            time.sleep(1)

        if env.winner in n_wins:
            n_wins[env.winner] += 1
            n_played += 1
        if not graphics.running: break

    print('Results:')
    print(f'black won {100.0 * n_wins[1] / n_played}% Nbr blacks: {np.sum(env.board == 1)}')
    print(f'white won {100.0 * n_wins[-1] / n_played}% Nbr whites: {np.sum(env.board == -1)}')
    print(f'draw {100.0 * n_wins[0] / n_played}% Nbr blanks: {np.sum(env.board == 0)}')

    time.sleep(1)

if __name__ == '__main__': main()
