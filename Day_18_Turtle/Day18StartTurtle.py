from turtle import Turtle, Screen

# timmy_the_the_turtle = Turtle()
# timmy_the_the_turtle.shape("turtle")
# timmy_the_the_turtle.color("blue")
# timmy_the_the_turtle.forward(100)
# timmy_the_the_turtle.right(90)

######## Challenge 1 - Draw a Square ############
import turtle as t

timmy_the_turtle = t.Turtle()

for _ in range(4):
    timmy_the_turtle.forward(100)
    timmy_the_turtle.left(90)


screen = Screen()
screen.exitonclick()