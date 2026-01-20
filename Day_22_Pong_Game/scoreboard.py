from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self._draw_net()
        self.update_scoreboard()

    def _draw_net(self):
        # dashed center line
        self.goto(0, 300)
        self.setheading(270)
        for _ in range(15):
            self.pendown()
            self.forward(20)
            self.penup()
            self.forward(20)

    def update_scoreboard(self):
        self.clear()  # clears everything this turtle drew (not the net since it was drawn before clear)
        # redraw net after clear
        self._draw_net()

        self.goto(-100, 240)
        self.write(self.l_score, align="center", font=("Courier", 40, "bold"))
        self.goto(100, 240)
        self.write(self.r_score, align="center", font=("Courier", 40, "bold"))

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()

    def game_over(self, winner):
        self.goto(0, 0)
        self.write(f"GAME OVER\n{winner} Player Wins!\n\nClick to exit",
                   align="center", font=("Courier", 24, "bold"))
