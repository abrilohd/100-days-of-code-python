from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

def move_forward():
    tim.forward(10)

def move_backward():
    tim.backward(10)

def turn_left():
    # tim.heading()
    # tim.left(10)
    # tim.heading()
    # # or work by this
    new_heading = tim.heading() + 10
    tim.setheading(new_heading)

def turn_right():
    # tim.heading()
    # tim.right(10)
    # tim.heading()
    # or work by this
    new_heading = tim.heading() - 10
    tim.setheading(new_heading)

def clear_drawing():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

screen.listen()
screen.onkey(key="w", fun=move_forward)
screen.onkey(key="s", fun=move_backward)
screen.onkey(key="a", fun=turn_left)
screen.onkey(key="d", fun=turn_right)
screen.onkey(key="c", fun=clear_drawing )
screen.exitonclick()