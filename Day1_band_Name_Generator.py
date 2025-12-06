"""Day 1 — Band Name Generator

A tiny interactive script that suggests a band name using the city you grew up in
and your pet's name, and demonstrates string length counting.

Run:
    python day-1/day1_band_name_generator.py
"""

def get_nonempty_input(prompt: str) -> str:
    """Ask the user for input until they type something non-empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value (cannot be empty).")


def main() -> None:
    print("Welcome to the Band Name Generator!\n")

    city = get_nonempty_input("What is the name of the city you grew up in? ")
    pet = get_nonempty_input("What is your pet's name? ")

    # Create a friendly band name (title case)
    band_name = f"{city.strip().title()} {pet.strip().title()}"
    print(f"\nYour band name could be: {band_name}\n")

    # Demonstrate len() on user-provided string
    sample = input("Enter a word to count its characters (or press Enter to skip): ").strip()
    if sample:
        print(f"The length of '{sample}' is {len(sample)} characters.")
    else:
        print("No sample provided — skipping length count.")


if __name__ == "__main__":
    main()
