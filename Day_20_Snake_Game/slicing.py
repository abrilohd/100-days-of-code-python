# Mini Word Analyzer using slicing

# 1. Take user input
word = input("Enter a word: ")

# 2. First half
first_half = word[:len(word)//2]

# 3. Last half
last_half = word[len(word)//2:]

# 4. Reverse the word
reversed_word = word[::-1]

# 5. Every second letter
every_second = word[::2]

# 6. Display results
print("\n--- Word Analysis ---")
print(f"Original word: {word}")
print(f"First half: {first_half}")
print(f"Last half: {last_half}")
print(f"Reversed word: {reversed_word}")
print(f"Every 2nd letter: {every_second}")
