import random
from Day12Art import logo
EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5
def check_answer(guess, answer, turns):
    if guess > answer:
        print("Too High.")
        return turns - 1
    elif guess < answer:
        print("Too Low.")
        return turns - 1
    else:
        print(f"you Got it. The answer is {answer}.")

def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if level == "easy":
        return EASY_LEVEL_TURNS
    else:
        return HARD_LEVEL_TURNS
def Game():
    print(logo)
    print("Wellcome to the number guessing Game!")
    print("I'am Thinking of a number between 1 and 100.")
    answer = random.randint(1, 100)

    turns = set_difficulty()

    guess = 0
    while guess != answer:
        print(f"You have {turns} attempts remaing to guess the number.")
        guess = int(input("Make a guess: "))
        turns = check_answer(guess, answer, turns)
        if turns == 0:
            print("You have run out guess <You Lose>. ")
            return
        elif guess != answer:
            print("Guess again")
        
Game()