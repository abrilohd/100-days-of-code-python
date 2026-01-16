# import turtle
# tim = turtle.Turtle()

# # from turtle import *     #import Everything
# tim = Turtle()
# tom = Turtle()
# terry = Turtle()

from turtle import Screen
import turtle as t       # as t=> alies name, like represent turtle as t
tim = t.Turtle()
screen = Screen()
import random

########### Challenge 2 - Draw a Dashed Line ########
# for _ in range(50):
#     tim.forward(10)
#     tim.penup()
#     tim.forward(10)
#     tim.pendown()

########### Challenge 3 - Draw Shapes ########
# colors = ["red", "blue", "green", "yellow", "purple", "orange", "black", "pink", "brown"]
# num_sides = 3
# for _ in range(num_sides, 11):
#     tim.color(random.choice(colors))
#     angle = 360 / num_sides
#     for shape in range(num_sides):
#         tim.forward(100)
#         tim.right(angle)
#     num_sides += 1


########### Challenge 4 - Random Walk ########
# colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
# directions = [0, 90, 180, 270]
# tim.pensize(15)
# tim.speed(10)    or tim.speed("fastest")

# for _ in range(200):
#     tim.color(random.choice(colours))
#     tim.forward(30)
#     tim.setheading(random.choice(directions))


t.colormode(255)
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

########### Challenge 5 - Spirograph ########

def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tim.speed(15)
        tim.color(random_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)

draw_spirograph(5)


screen.exitonclick()