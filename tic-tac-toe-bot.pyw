#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===== Tic-Tac-Toe mit unschlagbarer KI – wählbares Symbol =====
# Du kannst vor dem Spiel auswählen, ob du X (beginnt) oder O (zweiter) sein möchtest.
# Die KI spielt immer das andere Symbol und ist unschlagbar.

import tkinter as tk
from tkinter import messagebox
import itertools

class TicTacToe:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol          # "X" oder "O"
        self.ai_symbol = "O" if player_symbol == "X" else "X"
        self.root = tk.Tk()
        self.root.title(f"Tic-Tac-Toe – Du spielst {self.player_symbol}")
        self.root.resizable(False, False)
        
        # Spielfeld
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"   # X beginnt immer
        self.game_over = False
        
        # Buttons
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.root, text=" ", font=("Helvetica", 24, "bold"),
                                width=4, height=2, command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # Statusleiste
        self.status_label = tk.Label(self.root, text=self.get_status_text(), font=("Helvetica", 12))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Neustart-Button
        restart_btn = tk.Button(self.root, text="Neustart", font=("Helvetica", 10),
                                command=self.reset_game)
        restart_btn.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Wenn der Spieler O ist (KI beginnt), dann starte KI-Zug
        if self.current_player != self.player_symbol:
            self.root.after(500, self.ai_move)   # KI macht ersten Zug nach kurzer Pause
        
        self.root.mainloop()
    
    def get_status_text(self):
        if self.game_over:
            return "Spiel beendet"
        if self.current_player == self.player_symbol:
            return f"Du bist dran ({self.player_symbol})"
        else:
            return f"KI denkt nach... ({self.ai_symbol})"
    
    # ------------------------------------------------------------
    # Spielerzug
    # ------------------------------------------------------------
    def player_move(self, row, col):
        if self.game_over:
            return
        if self.current_player != self.player_symbol:
            return  # Nicht Spielers Zug
        if self.board[row][col] == " ":
            self.make_move(row, col, self.player_symbol)
            if not self.game_over:
                self.current_player = self.ai_symbol
                self.status_label.config(text=self.get_status_text())
                self.root.after(100, self.ai_move)   # KI starten
    
    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state="disabled")
        
        if self.check_win(player):
            self.game_over = True
            if player == self.player_symbol:
                messagebox.showinfo("Spielende", "Du hast gewonnen! 😮")
            else:
                messagebox.showinfo("Spielende", "KI hat gewonnen! 🤖")
            self.disable_all_buttons()
        elif self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Spielende", "Unentschieden!")
        else:
            # Spieler wechseln ist bereits außerhalb gesetzt
            pass
    
    # ------------------------------------------------------------
    # KI-Zug (Minimax)
    # ------------------------------------------------------------
    def ai_move(self):
        if self.game_over:
            return
        if self.current_player != self.ai_symbol:
            return  # Nicht KIs Zug
        
        best_score = -float("inf")
        best_move = None
        
        # Alle leeren Felder durchprobieren
        for i, j in itertools.product(range(3), range(3)):
            if self.board[i][j] == " ":
                self.board[i][j] = self.ai_symbol   # KI probiert
                score = self.minimax(self.board, 0, False)  # False = Minimierer (Spieler) ist dran
                self.board[i][j] = " "   # Zurücksetzen
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], self.ai_symbol)
            if not self.game_over:
                self.current_player = self.player_symbol
                self.status_label.config(text=self.get_status_text())
    
    def minimax(self, board, depth, is_maximizing):
        """
        Minimax-Algorithmus.
        - is_maximizing = True: Zug des KI-Spielers (ai_symbol)
        - is_maximizing = False: Zug des menschlichen Spielers (player_symbol)
        """
        # Gewinnbedingungen prüfen
        if self.check_win_on_board(board, self.ai_symbol):
            return 10 - depth
        if self.check_win_on_board(board, self.player_symbol):
            return -10 + depth
        if all(board[i][j] != " " for i, j in itertools.product(range(3), range(3))):
            return 0
        
        if is_maximizing:
            best = -float("inf")
            for i, j in itertools.product(range(3), range(3)):
                if board[i][j] == " ":
                    board[i][j] = self.ai_symbol
                    best = max(best, self.minimax(board, depth+1, False))
                    board[i][j] = " "
            return best
        else:
            best = float("inf")
            for i, j in itertools.product(range(3), range(3)):
                if board[i][j] == " ":
                    board[i][j] = self.player_symbol
                    best = min(best, self.minimax(board, depth+1, True))
                    board[i][j] = " "
            return best
    
    # ------------------------------------------------------------
    # Hilfsfunktionen
    # ------------------------------------------------------------
    def check_win(self, player):
        return self.check_win_on_board(self.board, player)
    
    def check_win_on_board(self, board, player):
        # Zeilen
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
        # Spalten
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return True
        # Diagonalen
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def is_board_full(self):
        return all(self.board[i][j] != " " for i, j in itertools.product(range(3), range(3)))
    
    def disable_all_buttons(self):
        for i, j in itertools.product(range(3), range(3)):
            self.buttons[i][j].config(state="disabled")
    
    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"   # X beginnt immer
        self.game_over = False
        for i, j in itertools.product(range(3), range(3)):
            self.buttons[i][j].config(text=" ", state="normal")
        self.status_label.config(text=self.get_status_text())
        
        # Wenn Spieler O ist, muss KI beginnen
        if self.current_player != self.player_symbol:
            self.root.after(500, self.ai_move)

# ------------------------------------------------------------
# Startdialog zur Symbolauswahl
# ------------------------------------------------------------
def start_dialog():
    dialog = tk.Tk()
    dialog.title("Tic-Tac-Toe")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    
    tk.Label(dialog, text="Wähle dein Symbol:", font=("Helvetica", 12)).pack(pady=20)
    
    def select_x():
        dialog.destroy()
        TicTacToe("X")
    
    def select_o():
        dialog.destroy()
        TicTacToe("O")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="X (beginnt)", font=("Helvetica", 11), command=select_x, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="O (spielt nach KI)", font=("Helvetica", 11), command=select_o, width=15).pack(side="left", padx=5)
    
    dialog.mainloop()

if __name__ == "__main__":
    start_dialog()
