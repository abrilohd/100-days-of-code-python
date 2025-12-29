import random
import string

def generate_password(num_letters, num_symbols, num_numbers):
    """Generate a strong, random password with the given character counts."""
    
    letters = list(string.ascii_letters)
    symbols = list("!@#$%^&*()+")
    numbers = list(string.digits)

    password_chars = []

    # Add random letters
    for _ in range(num_letters):
        password_chars.append(random.choice(letters))

    # Add random symbols
    for _ in range(num_symbols):
        password_chars.append(random.choice(symbols))

    # Add random numbers
    for _ in range(num_numbers):
        password_chars.append(random.choice(numbers))

    # Shuffle the resulting list
    random.shuffle(password_chars)

    # Join to form the final password string
    return ''.join(password_chars)


def main():
    print("🔐 Welcome to the PyPassword Generator!")

    try:
        num_letters = int(input("How many letters would you like in your password? "))
        num_symbols = int(input("How many symbols would you like in your password? "))
        num_numbers = int(input("How many numbers would you like in your password? "))
    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    if num_letters < 0 or num_symbols < 0 or num_numbers < 0:
        print("❌ Values must be non-negative.")
        return

    password = generate_password(num_letters, num_symbols, num_numbers)

    print(f"\n✅ Your generated password is: {password}")

    try:
        import pyperclip
        pyperclip.copy(password)
        print("📋 Password copied to clipboard!")
    except ImportError:
        print("ℹ️ Install 'pyperclip' to enable clipboard support: pip install pyperclip")


if __name__ == "__main__":
    main()
