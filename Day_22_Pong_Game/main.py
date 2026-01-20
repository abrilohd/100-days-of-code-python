from turtle import Screen, Turtle
import time

# --------- Constants ----------
WIDTH, HEIGHT = 800, 600
WIN_SCORE = 10
PADDLE_MOVE = 30
PADDLE_STRETCH_WID = 5  # 5 * 20px = 100px tall
BALL_START_SPEED = 0.09

# --------- Paddle Class ----------
class Paddle(Turtle):
    def __init__(self, position, screen_height=HEIGHT):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed("fastest")
        self.shapesize(stretch_wid=PADDLE_STRETCH_WID, stretch_len=1)
        self.goto(position)

        half_paddle = 10 * PADDLE_STRETCH_WID
        self.top_limit = (screen_height / 2) - half_paddle
        self.bottom_limit = -self.top_limit

    def go_up(self):
        new_y = self.ycor() + PADDLE_MOVE
        if new_y > self.top_limit:
            new_y = self.top_limit
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - PADDLE_MOVE
        if new_y < self.bottom_limit:
            new_y = self.bottom_limit
        self.goto(self.xcor(), new_y)

# --------- Ball Class ----------
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = BALL_START_SPEED

    def move(self):
        self.goto(self.xcor() + self.x_move, self.ycor() + self.y_move)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        # Increase speed slightly but cap at 0.015
        self.move_speed = max(0.015, self.move_speed * 0.9)

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = BALL_START_SPEED
        self.bounce_x()  # Serve toward the player who scored last

# --------- Scoreboard Class ----------
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-100, HEIGHT/2 - 60)
        self.write(self.l_score, align="center", font=("Courier", 40, "bold"))
        self.goto(100, HEIGHT/2 - 60)
        self.write(self.r_score, align="center", font=("Courier", 40, "bold"))

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()

    def game_over(self, winner):
        self.goto(0, 0)
        self.write(f"GAME OVER\n{winner} Player Wins!\nClick to exit",
                   align="center", font=("Courier", 24, "bold"))

# --------- Start Screen ----------
def show_start_screen(screen):
    banner = Turtle(visible=False)
    banner.color("white")
    banner.penup()
    banner.goto(0, 130)
    banner.write("P O N G", align="center", font=("Courier", 48, "bold"))
    banner.goto(0, 60)
    banner.write("Left: W / S    Right: Up / Down", align="center", font=("Courier", 18, "normal"))
    banner.goto(0, 25)
    banner.write("First to 10 points wins", align="center", font=("Courier", 16, "normal"))
    banner.goto(0, -25)
    banner.write("Press SPACE to start", align="center", font=("Courier", 18, "bold"))
    return banner

# --------- Screen ----------
screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.title("🏓 Pong")
screen.tracer(0)

# Show start screen and wait for SPACE
banner = show_start_screen(screen)
game_started = False
def start_game():
    global game_started
    game_started = True
    banner.clear()

screen.listen()
screen.onkey(start_game, "space")
while not game_started:
    screen.update()

# --------- Create Game Objects ----------
r_paddle = Paddle((WIDTH//2 - 50, 0))
l_paddle = Paddle((-WIDTH//2 + 50, 0))
ball = Ball()
scoreboard = Scoreboard()

# Paddle controls
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")

# --------- Main Game Loop ----------
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Collision with top/bottom walls
    if ball.ycor() > HEIGHT/2 - 10 or ball.ycor() < -HEIGHT/2 + 10:
        ball.bounce_y()

    # Collision with paddles
    if (ball.xcor() > WIDTH/2 - 60 and ball.distance(r_paddle) < 50) or \
       (ball.xcor() < -WIDTH/2 + 60 and ball.distance(l_paddle) < 50):
        ball.bounce_x()

    # Right paddle misses
    if ball.xcor() > WIDTH/2 - 20:
        ball.reset_position()
        scoreboard.l_point()

    # Left paddle misses
    if ball.xcor() < -WIDTH/2 + 20:
        ball.reset_position()
        scoreboard.r_point()

    # Check winning condition
    if scoreboard.l_score >= WIN_SCORE:
        scoreboard.game_over("Left")
        game_is_on = False
    elif scoreboard.r_score >= WIN_SCORE:
        scoreboard.game_over("Right")
        game_is_on = False

screen.exitonclick()
