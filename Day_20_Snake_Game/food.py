from turtle import Turtle
import random


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.6, stretch_wid=0.6)
        self.color("blue")
        self.refresh()

    def refresh(self):
        in_x = random.randint(-280, 280)
        in_y = random.randint(-280, 280)
        self.goto(in_x, in_y)