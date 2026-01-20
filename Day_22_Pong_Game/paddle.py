from turtle import Turtle

# Movement per key press & default paddle size
STEP = 30
STRETCH_WID = 5  # 20px turtle unit * 5 = 100px tall paddle

class Paddle(Turtle):
    def __init__(self, position, screen_height=600):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed("fastest")
        self.shapesize(stretch_wid=STRETCH_WID, stretch_len=1)
        self.goto(position)

        # Calculate dynamic limits so paddle never leaves screen
        half_paddle = 10 * STRETCH_WID  # 20px total height -> 10px half * stretch_wid
        self.top_limit = (screen_height / 2) - half_paddle
        self.bottom_limit = -self.top_limit

    def go_up(self):
        new_y = self.ycor() + STEP
        if new_y > self.top_limit:
            new_y = self.top_limit
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - STEP
        if new_y < self.bottom_limit:
            new_y = self.bottom_limit
        self.goto(self.xcor(), new_y)
