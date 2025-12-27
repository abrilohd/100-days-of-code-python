"""
Day 4 - Working with Lists
"""

states_of_america = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut",
    "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan",
    "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire",
    "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota",
    "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia",
    "wisconsin", "wyoming"
]

# Access last element
print("Last state:", states_of_america[-1])

# Add one item
states_of_america.append("other_state")

# Add multiple items
states_of_america.extend(["state_one", "state_two", "state_three"])

# Remove last items
states_of_america.pop()
states_of_america.pop()

print("Updated states list:")
print(states_of_america)
