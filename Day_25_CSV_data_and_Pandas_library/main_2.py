import turtle
import pandas
import time
import random

# --- SCREEN SETUP ---
screen = turtle.Screen()
screen.title("Ethiopia Regions Challenge")
image = "ethiopia_map.gif"
screen.addshape(image)
turtle.shape(image)

# --- DATA ---
data = pandas.read_csv("ethiopia_regions.csv")
print(data.iloc[0:10, 0:1])
all_regions = data.region.to_list()
guessed_regions = []
time_limit = 90  # 90 seconds to guess all
start_time = time.time()

# --- SCOREBOARD ---
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(-280, 260)
score_writer.color("blue")

def update_score():
    score_writer.clear()
    score_writer.write(f"Score: {len(guessed_regions)}/{len(all_regions)} | Time Left: {int(time_left)}s", align="left", font=("Arial", 14, "bold"))

# --- HINT SYSTEM ---
def give_hint():
    remaining = [r for r in all_regions if r not in guessed_regions]
    if remaining:
        hint = random.choice(remaining)[0]  # first letter
        screen.textinput(title="Hint", prompt=f"A region starts with '{hint}'")

screen.listen()
screen.onkey(give_hint, "h")  # Press 'H' for hint

# --- GAME LOOP ---
while len(guessed_regions) < len(all_regions):
    time_left = time_limit - (time.time() - start_time)
    if time_left <= 0:
        break

    update_score()
    answer_region = screen.textinput(title=f"{len(guessed_regions)}/{len(all_regions)} Regions Correct",
                                     prompt="Guess a region (or type 'Exit')").title()

    if answer_region == "Exit":
        break

    if answer_region in all_regions and answer_region not in guessed_regions:
        guessed_regions.append(answer_region)
        region_data = data[data.region == answer_region]
        marker = turtle.Turtle()
        marker.hideturtle()
        marker.penup()
        marker.goto(int(region_data.x), int(region_data.y))
        marker.write(answer_region, align="center", font=("Arial", 10, "normal"))

# --- GAME OVER ---
update_score()
end_text = turtle.Turtle()
end_text.hideturtle()
end_text.color("red")
end_text.penup()
end_text.goto(0, 0)

if len(guessed_regions) == len(all_regions):
    end_text.write("🎉 YOU WON! 🎉", align="center", font=("Arial", 24, "bold"))
else:
    end_text.write("⏳ TIME'S UP! GAME OVER ⏳", align="center", font=("Arial", 24, "bold"))

# Save missing regions
missing_regions = [region for region in all_regions if region not in guessed_regions]
pandas.DataFrame(missing_regions).to_csv("regions_to_learn.csv")
screen.mainloop()
