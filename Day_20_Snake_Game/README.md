# Day 20 – Snake Game (Core Mechanics) 🐍

## What I Learned
- How to split a game into multiple Python files (modules)
- How to design a game using classes (`Snake`, `Food`, `Scoreboard`)
- How to control game speed using `time.sleep()`
- How to detect collisions:
  - Snake with food
  - Snake with wall
  - Snake with its own tail
- How to manage game state (game running vs game over)

## Game Structure
- `main.py` → Main game loop and screen setup
- `snake.py` → Snake movement, body segments, and controls
- `food.py` → Food creation and random positioning
- `scoreboard.py` → Score display and game-over message

## Controls
- **Up Arrow** → Move up  
- **Down Arrow** → Move down  
- **Left Arrow** → Move left  
- **Right Arrow** → Move right  

## How the Game Works
- The snake moves continuously
- Eating food:
  - Increases score
  - Grows the snake
- Hitting the wall or tail ends the game

## Key Takeaway
This project shows how real games are built:
small classes working together inside one main loop.
