from turtle import *
# Square
t = Turtle()
screen = Screen()

def draw_s():
    for _ in range(4):
        t.forward(100)
        t.right(90)


screen.textinput("title", "prompt")
draw_s()
# Filled circle
t.begin_fill()
t.circle(50)
t.end_fill()

screen.exitonclick()