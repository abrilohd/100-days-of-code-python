# Day 21 – OOP Coffee Machine ☕

## What I Learned
- How to build a system using multiple interacting classes
- How objects communicate using methods instead of global logic
- How to separate responsibilities clearly in OOP design
- How to control program flow using a central controller (`main.py`)

## System Components
- `Menu` → Stores available drinks
- `MenuItem` → Represents a single drink with ingredients and cost
- `CoffeeMaker` → Manages resources and makes coffee
- `MoneyMachine` → Handles payment and money reporting
- `main.py` → Orchestrates interactions between all objects

## How the Program Works
1. Display available drink options
2. User selects:
   - A drink → system checks resources & payment
   - `report` → shows machine status
   - `off` → turns off the machine
3. If resources and payment are sufficient:
   - Coffee is made
   - Resources are updated
   - Money is recorded

## Key OOP Concepts Applied
- Encapsulation
- Object interaction
- Single Responsibility Principle
- Abstraction through methods

## Key Takeaway
Complex systems become simple when each object
has one clear responsibility and communicates properly.
