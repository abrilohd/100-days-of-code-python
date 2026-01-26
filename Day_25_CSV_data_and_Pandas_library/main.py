import turtle
import pandas as pd
import time
import os

# ------------------ CONSTANTS ------------------
IMAGE = "blank_states_img.gif"
STATES_FILE = "50_states.csv"
LEADERBOARD_FILE = "leaderboard.csv"
WRONG_GUESSES_FILE = "wrong_guesses.csv"
TIME_LIMIT = 180  # 3 minutes

# ------------------ SETUP ------------------
screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

data = pd.read_csv(STATES_FILE)
all_states = data.state.to_list()


# ------------------ FUNCTIONS ------------------
def get_missing_states(guessed_states):
    return [state for state in all_states if state not in guessed_states]


def mark_state_on_map(state_name):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    state_data = data[data.state == state_name]
    t.goto(int(state_data.x), int(state_data.y))
    t.write(state_name, align="center", font=("Arial", 8, "normal"))


def save_missing_states_to_csv(guessed_states):
    missing_states = get_missing_states(guessed_states)
    new_data = pd.DataFrame({"State": missing_states})
    new_data.to_csv("states_to_learn.csv", index=False)


def log_wrong_guess(guess):
    if os.path.exists(WRONG_GUESSES_FILE):
        wrong_data = pd.read_csv(WRONG_GUESSES_FILE)
    else:
        wrong_data = pd.DataFrame(columns=["Wrong Guess"])
    new_row = pd.DataFrame({"Wrong Guess": [guess]})
    wrong_data = pd.concat([wrong_data, new_row], ignore_index=True)
    wrong_data.to_csv(WRONG_GUESSES_FILE, index=False)


def update_leaderboard(name, time_taken, guessed_count):
    if os.path.exists(LEADERBOARD_FILE):
        leaderboard = pd.read_csv(LEADERBOARD_FILE)
    else:
        leaderboard = pd.DataFrame(columns=["Name", "Time Taken (s)", "States Guessed"])

    new_row = pd.DataFrame({"Name": [name], "Time Taken (s)": [time_taken], "States Guessed": [guessed_count]})
    leaderboard = pd.concat([leaderboard, new_row], ignore_index=True)

    # Sort by time if all states guessed, else by guessed count
    leaderboard.sort_values(by=["States Guessed", "Time Taken (s)"], ascending=[False, True], inplace=True)
    leaderboard.to_csv(LEADERBOARD_FILE, index=False)


def show_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        leaderboard = pd.read_csv(LEADERBOARD_FILE)
        print("\n🏆 Leaderboard:")
        print(leaderboard.head(10).to_string(index=False))
    else:
        print("\nNo leaderboard data yet.")


def play_game():
    guessed_states = []
    start_time = time.time()
    wrong_guesses = 0

    name = screen.textinput(title="Enter Name", prompt="Please enter your name for the leaderboard:") or "Player"

    while len(guessed_states) < 50:
        elapsed = int(time.time() - start_time)
        remaining_time = TIME_LIMIT - elapsed

        if remaining_time <= 0:
            screen.textinput(title="Time's Up!", prompt="⏳ Time is up! Press OK to see results.")
            break

        answer_state = screen.textinput(
            title=f"{len(guessed_states)}/50 States | Time Left: {remaining_time}s",
            prompt="Guess a state name (or type 'Exit' to quit):"
        )

        if answer_state is None:  # Closed dialog
            break

        answer_state = answer_state.title()

        if answer_state == "Exit":
            break

        if answer_state in all_states and answer_state not in guessed_states:
            guessed_states.append(answer_state)
            mark_state_on_map(answer_state)
        elif answer_state not in all_states:
            wrong_guesses += 1
            log_wrong_guess(answer_state)

    # Game over
    save_missing_states_to_csv(guessed_states)
    time_taken = int(time.time() - start_time)
    update_leaderboard(name, time_taken, len(guessed_states))

    # Show summary
    summary = f"You guessed {len(guessed_states)} states.\nWrong guesses: {wrong_guesses}\nTime: {time_taken}s"
    screen.textinput(title="Game Over", prompt=summary + "\nPress OK to continue.")
    show_leaderboard()


# ------------------ MAIN LOOP ------------------
while True:
    play_game()
    again = screen.textinput(title="Play Again?", prompt="Type Yes to play again, No to quit:") or "no"
    if again.lower() != "yes":
        break

screen.exitonclick()
