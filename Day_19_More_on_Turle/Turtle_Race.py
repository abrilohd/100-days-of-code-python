from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Wellcome To Simple Turtle Race GAME 🐢", prompt="Press Any Key To Start")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

#Create 6 turtlesfrom turtle import Turtle, Screen
import random
import time

screen = Screen()
screen.setup(width=600, height=400)
screen.bgcolor("lightblue")
screen.title("Turtle Race 🐢")

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-90, -60, -30, 0, 30, 60]
all_turtles = []
finish_line_x = 250

# Draw Finish Line
def draw_finish_line():
    line = Turtle()
    line.hideturtle()
    line.penup()
    line.goto(finish_line_x, -100)
    line.setheading(90)
    line.pendown()
    line.pensize(3)
    line.color("black")
    line.forward(200)

# Display message on screen
def show_message(message, color="black"):
    msg = Turtle()
    msg.hideturtle()
    msg.penup()
    msg.goto(0, 150)
    msg.color(color)
    msg.write(message, align="center", font=("Arial", 18, "bold"))

# Countdown before race
def countdown():
    count_turtle = Turtle()
    count_turtle.hideturtle()
    count_turtle.penup()
    count_turtle.goto(0, 0)
    count_turtle.color("black")
    for i in range(3, 0, -1):
        count_turtle.clear()
        count_turtle.write(f"{i}", align="center", font=("Arial", 36, "bold"))
        time.sleep(1)
    count_turtle.clear()
    count_turtle.write("GO!", align="center", font=("Arial", 32, "bold"))
    time.sleep(1)
    count_turtle.clear()

# Set up turtles
def create_turtles():
    all_turtles.clear()
    for i in range(6):
        t = Turtle(shape="turtle")
        t.color(colors[i])
        t.penup()
        t.goto(x=-280, y=y_positions[i])
        all_turtles.append(t)

# Run the race
def start_race():
    user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? (red, orange, yellow, green, blue, purple)").lower()
    if user_bet not in colors:
        show_message("Invalid color. Restart the game.", "red")
        return

    draw_finish_line()
    countdown()

    race_on = True
    speed_profile = [random.randint(1, 5) for _ in range(6)]  # Each turtle has different 'base speed'

    while race_on:
        for i, turtle in enumerate(all_turtles):
            move = random.randint(1, 10) + speed_profile[i]
            turtle.forward(move)

            if turtle.xcor() > finish_line_x:
                race_on = False
                winning_color = turtle.pencolor()
                if user_bet == winning_color:
                    show_message(f"You've WON! The {winning_color} turtle wins! 🏁", "green")
                else:
                    show_message(f"You've LOST. The {winning_color} turtle won the race.", "red")
                if user_bet == winning_color:
                    show_message(f"You've WON! The {winning_color} turtle wins! 🏁", "green")
                else:
                    show_message(f"You've LOST. The {winning_color} turtle won the race.", "red")

                # Ask user what to do next
                choice = screen.textinput("Race Finished", "Type 'r' to race again or 'q' to quit:")

                if choice == "r":
                    screen.clearscreen()
                    create_turtles()
                    setup_controls()
                    start_race()
                elif choice == "q":
                    screen.bye()
                else:
                    show_message("Invalid input. Closing game.", "red")
                    time.sleep(2)
                    screen.bye()

                break


# Clear and restart race
def reset_game():
    screen.clearscreen()
    screen.bgcolor("lightblue")
    create_turtles()
    draw_finish_line()
    start_race()

# Bind key to restart
def setup_controls():
    screen.listen()
    screen.onkey(reset_game, "r")
    screen.onkey(screen.bye, "q")  # Quit game with 'q'

# --- Main Setup ---
create_turtles()
setup_controls()
start_race()
screen.mainloop()

for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        #230 is 250 - half the width of the turtle.
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")

        #Make each turtle move a random amount.
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()