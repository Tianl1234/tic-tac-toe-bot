#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===== Tic-Tac-Toe mit unschlagbarer KI – GUI mit abgerundeten Ecken =====
# Basierend auf der Minimax-Implementierung von Clederson Cruz.
# Das Fenster hat abgerundete Ecken, eine eigene Titelleiste und ist verschiebbar.
# Du kannst wählen, ob du X oder O sein möchtest und wer beginnt.

import sys
import ctypes
import tkinter as tk
from tkinter import messagebox
from math import inf as infinity
from random import choice
import itertools

# ------------------------------------------------------------
# Konsole sofort verstecken (für .pyw)
# ------------------------------------------------------------
if sys.platform == "win32":
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.FreeConsole()

# ------------------------------------------------------------
# Hilfsfunktion für abgerundete Rechtecke (Canvas)
# ------------------------------------------------------------
def _create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1,
              x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2,
              x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2,
              x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_round_rect = _create_round_rect

# ------------------------------------------------------------
# Custom Fensterklasse mit abgerundeten Ecken und Titelleiste
# ------------------------------------------------------------
class RoundWindow:
    def __init__(self, width, height, title, bg_color="#2b2b2b", title_color="#ffffff"):
        self.root = tk.Toplevel() if tk._default_root else tk.Tk()
        self.root.overrideredirect(True)
        # self.root.attributes("-topmost", True)   # optional, kann aktiviert werden
        self.root.geometry(f"{width}x{height}+300+200")
        self.root.configure(bg=bg_color)
        
        # Canvas für Hintergrund mit abgerundeten Ecken
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_round_rect(5, 5, width-5, height-5, r=20, fill=bg_color, outline="#4a4a4a", width=2)
        
        # Eigene Titelleiste
        title_bar = tk.Frame(self.root, bg=bg_color, height=30)
        title_bar.place(x=10, y=10, width=width-20)
        
        title_label = tk.Label(title_bar, text=title, font=("Segoe UI", 10, "bold"),
                               fg=title_color, bg=bg_color)
        title_label.pack(side="left", padx=10)
        
        close_btn = tk.Button(title_bar, text="✕", font=("Segoe UI", 10, "bold"),
                              fg=title_color, bg=bg_color, bd=0, activebackground="#c42b1c",
                              activeforeground="white", cursor="hand2",
                              command=self.root.destroy)
        close_btn.pack(side="right", padx=10)
        
        # Verschieben der gesamten Titelleiste
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)
        
        # Innenbereich für Widgets (auf dem Canvas)
        self.inner_frame = tk.Frame(self.root, bg=bg_color)
        self.inner_frame.place(x=15, y=50, width=width-30, height=height-70)
        
    def start_move(self, event):
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()
    
    def do_move(self, event):
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.root.geometry(f"+{x}+{y}")

# ------------------------------------------------------------
# Hauptspielklasse (angepasst an Minimax-Logik mit -1,0,1)
# ------------------------------------------------------------
class TicTacToeGUI:
    def __init__(self, player_symbol, player_starts):
        """
        player_symbol: 'X' oder 'O'
        player_starts: True (Spieler beginnt) oder False (KI beginnt)
        """
        self.player_symbol = player_symbol
        self.player_starts = player_starts
        
        # Spieler-Kodierung: HUMAN = -1, COMP = +1 (wie im Konsolenskript)
        if player_symbol == 'X':
            self.HUMAN = -1
            self.COMP = +1
            self.human_char = 'X'
            self.comp_char = 'O'
        else:
            self.HUMAN = -1
            self.COMP = +1
            # Aber der Spieler hat O, Computer X – dann müssen wir die Rollen tauschen
            # Im Konsolenskript ist HUMAN immer -1, COMP +1, aber die Symbole sind variabel.
            # Das ist einfach: Wir lassen die Kodierung gleich, aber tauschen die Zuordnung.
            self.HUMAN = -1
            self.COMP = +1
            self.human_char = 'O'
            self.comp_char = 'X'
        
        # Board: 3x3 Liste mit 0 = leer, -1 = HUMAN, +1 = COMP
        self.board = [[0, 0, 0] for _ in range(3)]
        
        # Abgerundetes Fenster erstellen
        self.win = RoundWindow(350, 400, f"Tic-Tac-Toe – Du spielst {self.player_symbol}")
        self.root = self.win.root
        self.inner = self.win.inner_frame
        
        # Buttons für das Spielfeld
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.inner, text=" ", font=("Helvetica", 20, "bold"),
                                width=3, height=1, command=lambda r=i, c=j: self.player_move(r, c),
                                bg="#3c3f41", fg="white", bd=1, relief="solid",
                                activebackground="#4a4a4a", activeforeground="white")
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
        
        # Statusleiste
        self.status_label = tk.Label(self.inner, text="", font=("Segoe UI", 10),
                                      fg="white", bg=self.inner.cget('bg'))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)
        
        # Neustart-Button
        restart_btn = tk.Button(self.inner, text="Neustart", font=("Segoe UI", 10, "bold"),
                                command=self.restart, bg="#4CAF50", fg="white",
                                bd=0, padx=10, pady=2, cursor="hand2")
        restart_btn.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Spielstart: Wenn der Computer beginnt, macht er den ersten Zug
        self.game_over = False
        self.update_status()
        
        if not self.player_starts:
            self.root.after(500, self.computer_move)
    
    # ------------------------------------------------------------
    # Hilfsfunktionen für das Spiel
    # ------------------------------------------------------------
    def update_status(self):
        if self.game_over:
            return
        # Prüfen, wer dran ist: Wenn Anzahl der Züge von HUMAN und COMP gleich sind,
        # ist der Spieler dran, der begonnen hat. Wir können einfach zählen, wie viele
        # HUMAN-Züge und COMP-Züge gemacht wurden.
        moves_human = sum(row.count(self.HUMAN) for row in self.board)
        moves_comp = sum(row.count(self.COMP) for row in self.board)
        
        if moves_human == moves_comp:
            # Gleich viele Züge: Der Spieler, der begonnen hat, ist dran
            if self.player_starts:
                self.status_label.config(text=f"Du bist dran ({self.human_char})")
            else:
                self.status_label.config(text=f"KI denkt... ({self.comp_char})")
        else:
            # Ungleiche Züge: Der andere ist dran
            if self.player_starts:
                self.status_label.config(text=f"KI denkt... ({self.comp_char})")
            else:
                self.status_label.config(text=f"Du bist dran ({self.human_char})")
    
    def player_move(self, row, col):
        if self.game_over:
            return
        
        # Prüfen, ob Spieler am Zug ist
        moves_human = sum(row.count(self.HUMAN) for row in self.board)
        moves_comp = sum(row.count(self.COMP) for row in self.board)
        
        if self.player_starts:
            if moves_human != moves_comp:
                return  # Nicht Spielers Zug
        else:
            if moves_human == moves_comp:
                return  # Nicht Spielers Zug (Computer ist dran)
        
        if self.board[row][col] != 0:
            return  # Feld bereits belegt
        
        # Zug ausführen
        self.board[row][col] = self.HUMAN
        self.buttons[row][col].config(text=self.human_char, state="disabled")
        
        # Prüfen auf Sieg oder Unentschieden
        if self.wins(self.board, self.HUMAN):
            self.game_over = True
            messagebox.showinfo("Spielende", "Du hast gewonnen! 😮")
            self.disable_all_buttons()
        elif self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Spielende", "Unentschieden!")
        else:
            # Computer ist dran
            self.update_status()
            self.root.after(100, self.computer_move)
    
    def computer_move(self):
        if self.game_over:
            return
        
        # Prüfen, ob Computer am Zug ist
        moves_human = sum(row.count(self.HUMAN) for row in self.board)
        moves_comp = sum(row.count(self.COMP) for row in self.board)
        
        if self.player_starts:
            if moves_human == moves_comp:
                return  # Nicht Computers Zug
        else:
            if moves_human != moves_comp:
                return  # Nicht Computers Zug
        
        depth = len(self.empty_cells())
        if depth == 0:
            return
        
        # Wenn das Board leer ist (depth == 9), wähle zufälligen Zug (wie im Konsolenskript)
        if depth == 9:
            x, y = choice([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)])
        else:
            move = self.minimax(self.board, depth, self.COMP)
            x, y = move[0], move[1]
        
        self.board[x][y] = self.COMP
        self.buttons[x][y].config(text=self.comp_char, state="disabled")
        
        # Prüfen auf Sieg oder Unentschieden
        if self.wins(self.board, self.COMP):
            self.game_over = True
            messagebox.showinfo("Spielende", "KI hat gewonnen! 🤖")
            self.disable_all_buttons()
        elif self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Spielende", "Unentschieden!")
        else:
            self.update_status()
    
    # ------------------------------------------------------------
    # Minimax-Implementierung (angepasst aus dem Konsolenskript)
    # ------------------------------------------------------------
    def wins(self, state, player):
        """
        Prüft, ob der Spieler (player = -1 oder +1) gewonnen hat.
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        return [player, player, player] in win_state
    
    def game_over_state(self, state):
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)
    
    def empty_cells(self):
        cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    cells.append([i, j])
        return cells
    
    def evaluate(self, state):
        if self.wins(state, self.COMP):
            return +1
        elif self.wins(state, self.HUMAN):
            return -1
        else:
            return 0
    
    def minimax(self, state, depth, player):
        """
        player: +1 für Computer, -1 für Mensch
        Rückgabe: Liste [beste_row, beste_col, bester_score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]
        
        if depth == 0 or self.game_over_state(state):
            score = self.evaluate(state)
            return [-1, -1, score]
        
        for cell in self.empty_cells_from_state(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y
            
            if player == self.COMP:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        
        return best
    
    def empty_cells_from_state(self, state):
        cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    cells.append([i, j])
        return cells
    
    # ------------------------------------------------------------
    # Hilfsfunktionen für die GUI
    # ------------------------------------------------------------
    def is_board_full(self):
        return all(self.board[i][j] != 0 for i, j in itertools.product(range(3), range(3)))
    
    def disable_all_buttons(self):
        for i, j in itertools.product(range(3), range(3)):
            self.buttons[i][j].config(state="disabled")
    
    def restart(self):
        self.root.destroy()
        start_dialog()

# ------------------------------------------------------------
# Startdialog mit abgerundeten Ecken
# ------------------------------------------------------------
def start_dialog():
    win = RoundWindow(400, 250, "Tic-Tac-Toe – Einstellungen")
    root = win.root
    inner = win.inner_frame
    
    # Überschrift
    tk.Label(inner, text="Wähle dein Symbol und wer beginnt", font=("Segoe UI", 11),
             fg="white", bg=inner.cget('bg')).pack(pady=10)
    
    # Frame für Symbolauswahl
    sym_frame = tk.Frame(inner, bg=inner.cget('bg'))
    sym_frame.pack(pady=5)
    tk.Label(sym_frame, text="Symbol:", font=("Segoe UI", 10), fg="white", bg=inner.cget('bg')).pack(side="left", padx=5)
    
    symbol_var = tk.StringVar(value="X")
    rb_x = tk.Radiobutton(sym_frame, text="X", variable=symbol_var, value="X",
                          bg=inner.cget('bg'), fg="white", selectcolor="#2b2b2b",
                          activebackground="#4a4a4a", activeforeground="white")
    rb_x.pack(side="left", padx=5)
    rb_o = tk.Radiobutton(sym_frame, text="O", variable=symbol_var, value="O",
                          bg=inner.cget('bg'), fg="white", selectcolor="#2b2b2b",
                          activebackground="#4a4a4a", activeforeground="white")
    rb_o.pack(side="left", padx=5)
    
    # Frame für Startspieler
    start_frame = tk.Frame(inner, bg=inner.cget('bg'))
    start_frame.pack(pady=5)
    tk.Label(start_frame, text="Beginnt:", font=("Segoe UI", 10), fg="white", bg=inner.cget('bg')).pack(side="left", padx=5)
    
    start_var = tk.StringVar(value="player")
    rb_player = tk.Radiobutton(start_frame, text="Du", variable=start_var, value="player",
                               bg=inner.cget('bg'), fg="white", selectcolor="#2b2b2b",
                               activebackground="#4a4a4a", activeforeground="white")
    rb_player.pack(side="left", padx=5)
    rb_ai = tk.Radiobutton(start_frame, text="KI", variable=start_var, value="ai",
                           bg=inner.cget('bg'), fg="white", selectcolor="#2b2b2b",
                           activebackground="#4a4a4a", activeforeground="white")
    rb_ai.pack(side="left", padx=5)
    
    # Info-Text
    info_text = "Hinweis: Wählst du O, spielt die KI mit X.\nWählst du X, spielt die KI mit O."
    tk.Label(inner, text=info_text, font=("Segoe UI", 8), fg="#aaaaaa", bg=inner.cget('bg')).pack(pady=10)
    
    def start_game():
        symbol = symbol_var.get()
        starts = start_var.get() == "player"
        root.destroy()
        TicTacToeGUI(symbol, starts)
    
    tk.Button(inner, text="Spiel starten", font=("Segoe UI", 11, "bold"),
              command=start_game, bg="#4CAF50", fg="white",
              bd=0, padx=20, pady=5, cursor="hand2").pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    start_dialog()
