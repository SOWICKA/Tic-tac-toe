import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

def show_welcome_screen():
    welcome_window = tk.Toplevel(window)
    welcome_window.title("Witaj w grze Kółko i Krzyżyk")
    welcome_window.focus_force()

    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    position_right = int(window.winfo_screenwidth()/2 - window_width/2)
    position_down = int(window.winfo_screenheight()/2 - window_height/2)
    welcome_window.geometry(f"+{position_right}+{position_down}")

    welcome_message = tk.Label(welcome_window, text="Witaj w grze Kółko i Krzyżyk!\n\n"
                                                    "Zasady gry są proste:\n"
                                                    "- Gra toczy się na planszy 3x3.\n"
                                                    "- Gracze wybierają na zmianę, gdzie umieścić swój symbol (X lub O).\n"
                                                    "- Wygrywa ten, kto pierwszy ustawi trzy swoje symbole w linii (poziomo, pionowo lub po skosie).\n"
                                                    "- Możesz grać przeciwko innemu graczowi lub komputerowi.\n\n"
                                                    "Miłej zabawy!", justify=tk.LEFT)
    welcome_message.pack(pady=10)

    start_button = tk.Button(welcome_window, text="Rozpocznij grę", command=lambda: [welcome_window.destroy(), window.focus_force()])
    start_button.pack(pady=10)

def draw_board():
    for i in range(3):
        for j in range(3):
            button_style = {'font': ('Helvetica', 24), 'bg': 'lightgray', 'activebackground': 'gray'}
            board_buttons[i][j] = tk.Button(window, text=" ", **button_style, height=2, width=5,
                                            command=lambda i=i, j=j: on_button_click(i, j))
            board_buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

def on_button_click(row, col):
    global current_player
    if board[row][col] == " " and not game_over:
        make_move(row, col, current_player)
        check_game_status()
        if not game_over:
            switch_player()
            update_current_player_label()
            if game_mode.get() == "Gracz vs Komputer" and current_player == "O":
                computer_move()
                check_game_status()
                if not game_over:
                    switch_player()
                    update_current_player_label()

def make_move(row, col, player):
    board[row][col] = player
    board_buttons[row][col].config(text=player)

def update_current_player_label():
    if not game_over:
        current_player_label.config(text=f"Aktualny gracz: {current_player}")
    else:
        current_player_label.config(text="Gra zakończona")

def reset_game():
    global current_player, game_over
    current_player = "X"
    game_over = False
    for i in range(3):
        for j in range(3):
            board[i][j] = " "
            board_buttons[i][j].config(text=" ", state=tk.NORMAL)
    update_current_player_label()
    reset_button.config(state=tk.DISABLED)

def computer_move():
    if validate_combobox(difficulty, ["Łatwy", "Średni", "Trudny"]):
        if difficulty.get() == "Łatwy":
            random_move()
        elif difficulty.get() == "Średni":
            medium_move()
        else:
            hard_move()

def random_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        make_move(row, col, "O")

def medium_move():
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_win('O'):
                    make_move(i, j, "O")
                    return
                board[i][j] = " "

                board[i][j] = "X"
                if check_win('X'):
                    make_move(i, j, "O")
                    return
                board[i][j] = " "

    random_move()

def hard_move():
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        make_move(best_move[0], best_move[1], 'O')

def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 1
    elif check_win('X'):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'O'
                    score = minimax(board, depth - 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'X'
                    score = minimax(board, depth - 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def check_game_status():
    global game_over
    if check_win(current_player):
        messagebox.showinfo("Koniec gry", f"Gracz {current_player} wygrywa!")
        game_over = True
        update_current_player_label()
        reset_button.config(state=tk.NORMAL)
    elif is_board_full():
        messagebox.showinfo("Koniec gry", "Remis!")
        game_over = True
        update_current_player_label()
        reset_button.config(state=tk.NORMAL)

def check_win(player):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] == player or
            board[0][i] == board[1][i] == board[2][i] == player):
            return True
    if (board[0][0] == board[1][1] == board[2][2] == player or
        board[0][2] == board[1][1] == board[2][0] == player):
        return True
    return False

def is_board_full():
    for row in board:
        if " " in row:
            return False
    return True

def switch_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"

def validate_combobox(combobox, valid_values):
    """
    Walidacja, czy wartość w rozwijanej liście (Combobox) jest jedną z prawidłowych wartości.
    """
    return combobox.get() in valid_values


window = tk.Tk()
window.title("Kółko i Krzyżyk")

current_player_label = tk.Label(window, text="", font=('normal', 14))
current_player_label.grid(row=3, column=0, columnspan=3)


game_mode_label = tk.Label(window, text="Tryb gry:")
game_mode_label.grid(row=4, column=0, columnspan=2)

game_mode = ttk.Combobox(window, values=["Gracz vs Gracz", "Gracz vs Komputer"])
game_mode.grid(row=4, column=2)
game_mode.current(0)  # Domyślnie ustawia na "Gracz vs Gracz"

difficulty_label = tk.Label(window, text="Poziom trudności gry komputerem:")
difficulty_label.grid(row=5, column=0, columnspan=2)

difficulty = ttk.Combobox(window, values=["Łatwy", "Średni", "Trudny"])
difficulty.grid(row=5, column=2)
difficulty.current(0)  # Domyślnie ustawia na "Łatwy"


reset_button = tk.Button(window, text="Resetuj grę", font=('normal', 14), command=reset_game)
reset_button.grid(row=6, column=0, columnspan=3)
reset_button.config(state=tk.DISABLED)

current_player = "X"
game_over = False
board = [[" " for _ in range(3)] for _ in range(3)]
board_buttons = [[None for _ in range(3)] for _ in range(3)]

show_welcome_screen()
draw_board()

window.mainloop()
