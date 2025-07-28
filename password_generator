import random
import string


def generate_password(length=12, include_symbols=True, include_numbers=True, include_uppercase=True, include_lowercase=True):
    """Generate a secure random password with customizable options."""
    
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        return "Error: At least one character type must be selected"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("=== Password Generator ===")
    
    while True:
        try:
            length = int(input("Enter password length (default 12): ") or "12")
            if length < 1:
                print("Length must be at least 1")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    symbols = input("Include symbols? (y/n, default y): ").lower() != 'n'
    numbers = input("Include numbers? (y/n, default y): ").lower() != 'n'
    uppercase = input("Include uppercase? (y/n, default y): ").lower() != 'n'
    lowercase = input("Include lowercase? (y/n, default y): ").lower() != 'n'
    
    password = generate_password(length, symbols, numbers, uppercase, lowercase)
    print(f"\nGenerated password: {password}")
    
    # Generate multiple passwords
    count = int(input("\nHow many passwords to generate? (default 1): ") or "1")
    if count > 1:
        print(f"\n{count} passwords:")
        for i in range(count):
            print(f"{i+1}: {generate_password(length, symbols, numbers, uppercase, lowercase)}")

if __name__ == "__main__":
    main()
