import turtle
import random
import time
from playsound3 import playsound3
import threading

# --- Config ---
NUM_HEARTS = 3
MISS_LIMIT = 5

# --- Setup screen ---
screen = turtle.Screen()
screen.title("Catch the Heart 💘")
screen.bgcolor("black")
screen.setup(width=450, height=800)
screen.tracer(0)

# --- Score ---
score = 0
misses = 0
level = 1
heart_speed = 3

# --- Scoreboard ---
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(-250, 300)

def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}   Missed: {misses}   Level: {level}", font=("Arial", 16, "bold"))

update_score()

# --- Player ---
player = turtle.Turtle()
player.shape("turtle")
player.color("gold")
player.penup()
player.goto(0, -280)
player.setheading(90)
player.speed(0)

# --- Bullet ---
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("white")
bullet.shapesize(stretch_wid=0.5, stretch_len=2)
bullet.speed("fastest")
bullet.penup()
bullet.goto(0, -500)
bullet.setheading(90)
bullet.hideturtle()
bullet_state = "ready"

# --- Heart Shape Registration ---
screen.register_shape("heart", ((0,0), (10,10), (20,0), (10,-10)))
screen.addshape("image.gif")

# --- Create Hearts ---
hearts = []
for _ in range(NUM_HEARTS):
    h = turtle.Turtle()
    h.shape("heart")
    h.color("red")
    h.penup()
    h.goto(random.randint(-280, 280), random.randint(100, 300))
    h.speed(0)
    hearts.append(h)

# --- Controls ---
def move_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 20)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# --- Explosion Sound ---
def play_sound():
    try:
        playsound3  # Replace with your own file path
    except:
        pass  # Skip if no file

# --- Key bindings ---
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# --- Game Loop ---
running = True
while running:
    screen.update()

    # Move hearts
    for h in hearts:
        h.sety(h.ycor() - heart_speed)

        # Missed heart
        if h.ycor() < -320:
            h.goto(random.randint(-280, 280), 300)
            misses += 1
            update_score()
            if misses >= MISS_LIMIT:
                running = False

        # Bullet collision
        if bullet.distance(h) < 20 and bullet_state == "fire":
            threading.Thread(target=play_sound).start()
            h.goto(random.randint(-280, 280), 300)
            bullet.hideturtle()
            bullet_state = "ready"
            score += 1
            update_score()

            # Level up every 5 points
            if score % 5 == 0:
                level += 1
                heart_speed += 0.5

    # Move bullet
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + 20)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    time.sleep(0.05)

# --- Game Over ---
game_over = turtle.Turtle()
game_over.hideturtle()
game_over.color("white")
game_over.penup()
game_over.goto(-100, 0)
game_over.write("GAME OVER 💔", font=("Arial", 32, "bold"))
screen.mainloop()
