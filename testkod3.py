from tkinter import Tk, Canvas, N, W, E, S, simpledialog
import numpy as np
import time

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
        self.click_callbacks = []

        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3], self.board[4, 4] = -1, -1
        self.board[4, 3], self.board[3, 4] = 1, 1

        self.running = True
        self.root.update()

    def destroy(self, event):
        self.running = False

    def save_wh(self, event):
        self.w, self.h = event.width, event.height
        self.draw()

    def update(self):
        self.root.update()

    def register_click_callback(self, callback):
        self.click_callbacks.append(callback)

    def on_click(self, event):
        sq_w, sq_h = self.w // 8, self.h // 8
        row, col = event.y // sq_h, event.x // sq_w
        for f in self.click_callbacks:
            f(row, col)

    def draw(self, board=None):
        if board is not None:
            self.board = board

        sq_w, sq_h = self.w // 8, self.h // 8
        self.canvas.delete('all')

        for i in range(8):
            self.canvas.create_line(0, i * sq_h, self.w, i * sq_h, width=5)
            self.canvas.create_line(i * sq_w, 0, i * sq_w, self.h, width=5)

        for i in range(8):
            for j in range(8):
                val = self.board[i, j]
                if val == 1:
                    self.canvas.create_oval(j * sq_w + 10, i * sq_h + 10, (j + 1) * sq_w - 10, (i + 1) * sq_h - 10, fill="black")
                elif val == -1:
                    self.canvas.create_oval(j * sq_w + 10, i * sq_h + 10, (j + 1) * sq_w - 10, (i + 1) * sq_h - 10, fill="white")

        self.root.update()

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3], self.board[4, 4] = -1, -1
        self.board[4, 3], self.board[3, 4] = 1, 1
        self.winner = 0

    def get_board(self):
        return self.board.copy()

    def get_possible_moves(self, player):
        return possible_moves(self.board, player)

    def game_over(self):
        if np.sum(self.board == 0) == 0 or (not self.get_possible_moves(1) and not self.get_possible_moves(-1)):
            blacks, whites = np.sum(self.board == 1), np.sum(self.board == -1)
            self.winner = 1 if blacks > whites else -1 if whites > blacks else 0
            return True
        return False

    def reset(self):
        self.__init__()

    def make_move(self, move):
        row, col = move['put']
        self.board[row, col] = move['player']
        for r, c in move['flipped']:
            self.board[r, c] = move['player']

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
        while self.pos is None:
            self.ui.update()
        return self.pos

    def move(self, env):
        moves = possible_moves(env.get_board(), self.player)
        if not moves:
            return

        while True:
            pos = self.get_click()
            for move in moves:
                if move['put'] == pos:
                    env.make_move(move)
                    return

class EvalAlphaBeta:
    def __init__(self, player, max_depth=4):
        self.player = player
        self.max_depth = max_depth

    def move(self, env):
        moves = possible_moves(env.get_board(), self.player)
        if moves:
            env.make_move(moves[0])  # Simplified AI move for now

def possible_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i, j] == 0:
                moves.append({'player': player, 'put': (i, j), 'flipped': []})  # Placeholder logic
    return moves

def choose_color():
    root = Tk()
    root.withdraw()
    choice = simpledialog.askstring("Choose Color", "Enter 'black' or 'white':").strip().lower()
    return 1 if choice == 'black' else -1

def main():
    graphics = Graphics()
    env = Othello()

    human_color = choose_color()
    human = HumanPlayer(human_color, graphics)
    ai = EvalAlphaBeta(-human_color)

    players = {human_color: human, -human_color: ai}
    graphics.draw(env.get_board())

    while True:
        for player in [human_color, -human_color]:
            players[player].move(env)
            graphics.draw(env.get_board())
            if env.game_over():
                break
        if env.game_over():
            break

    winner_text = "Draw" if env.winner == 0 else ("Black Wins!" if env.winner == 1 else "White Wins!")
    graphics.canvas.create_text(400, 400, text=winner_text, font=("Arial", 40), fill="yellow")
    graphics.root.update()
    time.sleep(5)
    graphics.root.destroy()

if __name__ == '__main__':
    main()
