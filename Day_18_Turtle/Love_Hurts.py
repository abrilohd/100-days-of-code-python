import turtle
import time

# Screen setup
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Love Hurts 💘")

# Draw heart
heart = turtle.Turtle()
heart.hideturtle()
heart.speed('fastest')
heart.color("red", "red")
heart.pensize(10)

def draw_heart():
    heart.penup()
    heart.goto(0, -100)
    heart.pendown()
    heart.begin_fill()
    heart.left(140)
    heart.forward(180)

    for _ in range(200):
        heart.right(1)
        heart.forward(2)

    heart.left(120)

    for _ in range(200):
        heart.right(1)
        heart.forward(2)

    heart.forward(180)
    heart.end_fill()

draw_heart()

# Arrow setup
arrow = turtle.Turtle()
arrow.shape("triangle")
arrow.color("gold")
arrow.penup()
arrow.setheading(-30)
arrow.goto(-300, 200)
arrow.speed(1)

# Animate arrow flying
for _ in range(70):
    x, y = arrow.pos()
    arrow.goto(x + 6, y - 3)
    time.sleep(0.04)

# Draw arrow shaft
shaft = turtle.Turtle()
shaft.hideturtle()
shaft.speed("fastest")
shaft.color("gold")
shaft.pensize(4)
shaft.penup()
shaft.goto(-250, 100)
shaft.setheading(-30)
shaft.pendown()
shaft.forward(500)

# Arrowhead
shaft.begin_fill()
for _ in range(3):
    shaft.left(120)
    shaft.forward(20)
shaft.end_fill()

# Feathers
feather = turtle.Turtle()
feather.hideturtle()
feather.color("gold")
feather.pensize(2)
feather.penup()
feather.goto(-250, 100)
feather.setheading(-30)
feather.forward(10)

for angle in [-135, -150, -165]:
    feather.setheading(angle)
    feather.forward(20)
    feather.backward(20)
    feather.setheading(-30)
    feather.forward(10)

# Text
text = turtle.Turtle()
text.hideturtle()
text.color("red")
text.penup()
text.goto(-90, -220)
text.write("ልብ አለው ወዪስ  ልብ አልባ  💘", font=("Arial", 24, "bold"))

turtle.done()
