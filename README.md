# 🎮 Tic-Tac-Toe with Unbeatable AI

A classic Tic-Tac-Toe game with a graphical interface (tkinter) where you can choose to play as **X** or **O**. The AI uses the **Minimax algorithm** and is **unbeatable** – you can only win if you play perfectly, which forces a draw, or if the AI makes a mistake (which it never does). 😉

---

## ✨ Features

- **Choose your symbol** – start as X (first player) or O (second player).  
- **Unbeatable AI** – based on the Minimax algorithm, ensuring optimal moves every time.  
- **Clean GUI** – simple and intuitive interface with a status bar and restart button.  
- **No console window** – when saved as `.pyw`, runs silently without a terminal.  
- **Automatic first move** – if you choose O, the AI (playing X) makes the first move.  

---

## 📦 Installation & Dependencies

The script requires **Python 3.6+** and **tkinter** (which comes with Python by default).  
No additional libraries are needed – everything is built‑in.

---

## 🚀 How to Run

1. **Save the script** with the extension **`.pyw`** (e.g. `tictactoe.pyw`) to prevent a console window from appearing.  
2. **Double‑click** the file – a small dialog will ask you to choose your symbol.  
3. **Select** either **X** (you start) or **O** (AI starts).  
4. The main game window opens.  
   - If you chose X, you make the first move.  
   - If you chose O, the AI makes the first move.  
5. Click on any empty cell to place your mark. The AI responds immediately.  
6. The game ends when someone wins or the board is full (draw). A message box announces the result.  
7. Click **"Neustart"** to play again (with the same symbol choice).

---

## 🧠 How the AI Works (Minimax)

The AI uses the **Minimax algorithm**, a recursive decision‑making algorithm for two‑player games:

- It simulates **all possible future moves** for itself and the opponent.  
- It assumes the opponent (you) will always choose the **best possible move for themselves**.  
- It assigns a score to each outcome:  
  - **+10** if the AI wins  
  - **-10** if the player wins  
  - **0** for a draw  
- The score is adjusted by the depth (number of moves) so that the AI prefers quicker wins and tries to delay losses.  
- The AI then picks the move that **maximises its score** under the assumption that you will minimise it.  

Because Minimax explores every possible game state, the AI is **perfect** – it will never lose. The best you can hope for is a draw if you also play perfectly.

---

## 🎯 Game Rules

- Players take turns placing their symbol (X or O) in empty cells.  
- X always moves first.  
- The first player to get **three of their symbols in a row** (horizontally, vertically, or diagonally) wins.  
- If all nine cells are filled without a winner, the game is a draw.

---

## ⚙️ Customisation

You can easily change the appearance or behaviour by editing the script:

- **Font size / button size** – modify the `font` and `width/height` parameters in the `Button` creation.  
- **Colors** – add `fg` and `bg` options to the buttons or labels.  
- **AI delay** – adjust the `after(500, ...)` value to make the AI move faster or slower.  
- **Symbols** – replace `"X"` and `"O"` with any other characters (e.g. emojis, shapes).  

---

## 🐛 Troubleshooting

| Problem | Solution |
|--------|----------|
| **Nothing happens when I double‑click the `.pyw` file** | The script may have crashed. Run it as `.py` (with console) to see error messages. Make sure you have Python installed correctly. |
| **The AI seems too slow** | Minimax for Tic‑Tac‑Toe is extremely fast. If it feels slow, you can reduce the `after(100, ...)` delay in the player move function. |
| **I want to play against a friend instead of the AI** | That would require a completely different script (two‑player mode). You can ask me for a separate version! |
| **The restart button doesn't work** | Check the indentation of the `reset_game` method – it must be inside the class. |

---

## 📄 License

This script is provided as‑is, free to use and modify. No warranty.

---

Enjoy the game – and try to beat the unbeatable AI! 🤖🎲
