import tkinter as tk
import random
import time

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("MindSpark")
root.geometry("700x600")
root.configure(bg="#F2F5FC")

score = 0
best_score = 0
game_area = None


# ---------- COMMON FUNCTIONS ----------
def clear_screen():
    global game_area

    for widget in root.winfo_children():
        widget.destroy()

    game_area = tk.Frame(root, bg="#F2F5FC")
    game_area.pack(fill="both", expand=True, padx=20, pady=20)


def heading(title):
    tk.Label(
        game_area, text=title,
        font=("Arial", 24, "bold"),
        bg="#F2F5FC", fg="#24345C"
    ).pack(pady=15)


def message(text):
    tk.Label(
        game_area, text=text,
        font=("Arial", 13),
        bg="#F2F5FC", fg="#24345C",
        wraplength=550
    ).pack(pady=10)


def button(text, command):
    tk.Button(
        game_area, text=text, command=command,
        font=("Arial", 12, "bold"),
        bg="#526DAB", fg="white",
        activebackground="#40568B",
        activeforeground="white",
        relief="flat", padx=12, pady=8
    ).pack(pady=6)


def back_button():
    button("🏠 Home", home)


def show_result(title, points):
    clear_screen()
    heading(title)
    message("Your score: " + str(points))
    message("Best score: " + str(best_score))
    button("Play Again", lambda: start_game(title))
    back_button()


def add_score(points):
    global score, best_score
    score += points
    best_score = max(best_score, score)


# ---------- 1. MEMORY FLASH ----------
def memory_flash():
    clear_screen()
    heading("Memory Flash")

    sequence = []
    position = [0]
    colors = ["Red", "Blue", "Green", "Yellow"]
    points = [0]

    display = tk.Label(
        game_area, text="Remember the sequence!",
        font=("Arial", 16), bg="#F2F5FC"
    )
    display.pack(pady=15)

    def new_round():
        sequence.append(random.choice(colors))
        position[0] = 0

        display.config(
            text="  →  ".join(sequence),
            fg="#24345C"
        )

        game_area.after(1500, hide_sequence)

    def hide_sequence():
        display.config(text="Repeat the sequence!")
        show_buttons()

    def show_buttons():
        for widget in choices.winfo_children():
            widget.destroy()

        for color in colors:
            tk.Button(
                choices, text=color, width=10,
                bg=color.lower(), fg="white",
                command=lambda c=color: check(c)
            ).pack(side="left", padx=3, pady=10)

    choices = tk.Frame(game_area, bg="#F2F5FC")
    choices.pack()

    def check(color):
        if color == sequence[position[0]]:
            position[0] += 1

            if position[0] == len(sequence):
                points[0] += 1
                display.config(
                    text="Correct! Round " + str(points[0] + 1)
                )
                for widget in choices.winfo_children():
                    widget.destroy()

                game_area.after(800, new_round)
            else:
                display.config(text="Correct! Keep going.")
        else:
            add_score(points[0])
            show_result("Memory Flash", points[0])

    back_button()
    new_round()


# ---------- 2. REFLEX RUSH ----------
def reflex_rush():
    clear_screen()
    heading("Reflex Rush")
    message("Wait until the screen turns green, then click!")

    area = tk.Button(
        game_area, text="WAIT...",
        font=("Arial", 20, "bold"),
        width=20, height=4,
        bg="#D9DDE7"
    )
    area.pack(pady=25)

    state = {"ready": False, "start": 0, "after": None}

    def finish():
        if state["ready"]:
            reaction = round((time.time() - state["start"]) * 1000)
            add_score(max(1, 1000 - reaction) // 100)
            show_result(
                "Reflex Rush",
                reaction
            )

    def go():
        state["ready"] = True
        state["start"] = time.time()
        area.config(text="CLICK NOW!", bg="green")
        area.config(command=finish)

    def start():
        state["ready"] = False
        area.config(text="WAIT...", bg="#D9DDE7", command=None)
        delay = random.randint(1500, 4000)
        state["after"] = root.after(delay, go)

    area.config(command=start)
    back_button()


# ---------- 3. NUMBER DETECTIVE ----------
def number_detective():
    clear_screen()
    heading("Number Detective")

    level = [1]
    answer = [0]
    points = [0]

    question = tk.Label(
        game_area, font=("Arial", 20),
        bg="#F2F5FC"
    )
    question.pack(pady=20)

    entry = tk.Entry(game_area, font=("Arial", 16), justify="center")
    entry.pack(pady=10)

    feedback = tk.Label(game_area, bg="#F2F5FC", font=("Arial", 12))
    feedback.pack(pady=10)

    def new_question():
        entry.delete(0, tk.END)
        feedback.config(text="")

        start = random.randint(1, 10)
        step = random.randint(2, 5) * level[0]
        sequence = [start + step * i for i in range(4)]
        answer[0] = start + step * 4

        question.config(
            text=",  ".join(map(str, sequence)) + ",  ?"
        )

    def check():
        try:
            guess = int(entry.get())
        except ValueError:
            feedback.config(text="Enter a whole number.")
            return

        if guess == answer[0]:
            points[0] += 1
            level[0] += 1
            feedback.config(text="Correct! Next level.")
            new_question()
        else:
            add_score(points[0])
            show_result("Number Detective", points[0])

    button("Submit Answer", check)
    back_button()
    new_question()


# ---------- 4. COLOR CONFUSION ----------
def color_confusion():
    clear_screen()
    heading("Color Confusion")

    colors = ["RED", "BLUE", "GREEN", "PURPLE"]
    color_values = {
        "RED": "#E53935",
        "BLUE": "#1565C0",
        "GREEN": "#2E7D32",
        "PURPLE": "#8E24AA"
    }

    points = [0]
    answer = [""]
    word = tk.Label(
        game_area, font=("Arial", 30, "bold"),
        bg="#F2F5FC"
    )
    word.pack(pady=30)

    options = tk.Frame(game_area, bg="#F2F5FC")
    options.pack()

    def new_question():
        answer[0] = random.choice(colors)
        displayed_word = random.choice(colors)
        word.config(
            text=displayed_word,
            fg=color_values[answer[0]]
        )

        for widget in options.winfo_children():
            widget.destroy()

        for color in colors:
            tk.Button(
                options, text=color,
                command=lambda c=color: check(c),
                width=10
            ).pack(pady=3)

    def check(choice):
        if choice == answer[0]:
            points[0] += 1
            new_question()
        else:
            add_score(points[0])
            show_result("Color Confusion", points[0])

    message("Choose the TEXT COLOR, not the word!")
    back_button()
    new_question()


# ---------- 5. SECRET CODE ----------
def secret_code():
    clear_screen()
    heading("Secret Code")

    code = random.sample("0123456789", 3)
    attempts = [0]

    message("Guess the secret 3-digit code. Digits do not repeat.")

    entry = tk.Entry(game_area, font=("Arial", 18), justify="center")
    entry.pack(pady=10)

    feedback = tk.Label(
        game_area, font=("Arial", 12),
        bg="#F2F5FC", wraplength=500
    )
    feedback.pack(pady=10)

    def check():
        guess = entry.get().strip()

        if len(guess) != 3 or not guess.isdigit() or len(set(guess)) != 3:
            feedback.config(text="Enter 3 different digits.")
            return

        attempts[0] += 1
        correct_position = sum(
            guess[i] == code[i] for i in range(3)
        )
        correct_digit = sum(
            digit in code for digit in guess
        )

        if guess == "".join(code):
            add_score(max(1, 10 - attempts[0]))
            show_result("Secret Code", max(1, 10 - attempts[0]))
        elif attempts[0] >= 8:
            clear_screen()
            heading("Secret Code")
            message("Out of attempts! The code was " + "".join(code))
            button("Play Again", secret_code)
            back_button()
        else:
            misplaced = correct_digit - correct_position
            feedback.config(
                text=f"Correct position: {correct_position}\n"
                     f"Correct digit, wrong position: {misplaced}\n"
                     f"Attempts left: {8 - attempts[0]}"
            )

    button("Check Code", check)
    back_button()


# ---------- 6. ODD ONE OUT ----------
def odd_one_out():
    clear_screen()
    heading("Odd One Out")

    points = [0]
    target = [""]
    options = tk.Frame(game_area, bg="#F2F5FC")
    options.pack(pady=20)

    feedback = tk.Label(
        game_area, font=("Arial", 14),
        bg="#F2F5FC"
    )
    feedback.pack()

    def new_question():
        for widget in options.winfo_children():
            widget.destroy()

        items = ["🍎", "🍌", "🍇", "🍊", "🍓", "🍉"]
        common = random.choice(items)
        different = random.choice([x for x in items if x != common])
        choices = [common] * 5 + [different]
        random.shuffle(choices)
        target[0] = different

        for item in choices:
            tk.Button(
                options, text=item,
                font=("Arial", 20), width=4,
                command=lambda x=item: check(x)
            ).pack(side="left", padx=3, pady=5)

    def check(choice):
        if choice == target[0]:
            points[0] += 1
            feedback.config(text="Correct! Score: " + str(points[0]))
            new_question()
        else:
            add_score(points[0])
            show_result("Odd One Out", points[0])

    message("Find the item that appears only once.")
    back_button()
    new_question()


# ---------- GAME MENU ----------
games = {
    "Memory Flash": memory_flash,
    "Reflex Rush": reflex_rush,
    "Number Detective": number_detective,
    "Color Confusion": color_confusion,
    "Secret Code": secret_code,
    "Odd One Out": odd_one_out
}


def start_game(name):
    games[name]()


def home():
    clear_screen()
    heading("🧠 BRAIN GAMES")
    message("Challenge your brain. Improve your skills!")

    for name in games:
        button(name, lambda n=name: start_game(n))

    message("Current best score: " + str(best_score))


home()
root.mainloop()
