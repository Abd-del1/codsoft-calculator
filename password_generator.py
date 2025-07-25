#!/usr/bin/env python3
"""
A simple password generator utility.

This script allows a user to generate a random password by specifying
the desired length and selecting which character sets to include. The
generator uses Python's `random.SystemRandom` for cryptographically
secure randomness and draws characters from uppercase letters,
lowercase letters, digits, and punctuation symbols depending on the
user's choices.

Example usage::

    $ python password_generator.py
    Password Generator
    Enter the desired password length (positive integer): 12
    Include uppercase letters? (y/n): y
    Include lowercase letters? (y/n): y
    Include digits? (y/n): y
    Include symbols? (y/n): n
    Generated password: aB3dEfGh12Ik

"""

import random
import string


def generate_password(length: int,
                      use_uppercase: bool = True,
                      use_lowercase: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True) -> str:
    """Generate a random password with the given options.

    Args:
        length (int): The length of the password to generate. Must be > 0.
        use_uppercase (bool): Whether to include uppercase letters.
        use_lowercase (bool): Whether to include lowercase letters.
        use_digits (bool): Whether to include digits.
        use_symbols (bool): Whether to include punctuation symbols.

    Returns:
        str: A randomly generated password.

    Raises:
        ValueError: If no character sets are selected or length <= 0.
    """
    if length <= 0:
        raise ValueError("Password length must be a positive integer.")

    # Build the pool of characters to sample from.
    characters = ""
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError(
            "No character types selected. Enable at least one type of characters."
        )

    # Use a cryptographically secure random generator.
    secure_random = random.SystemRandom()
    return ''.join(secure_random.choice(characters) for _ in range(length))


def ask_yes_no(prompt: str) -> bool:
    """Prompt the user with a yes/no question and return a boolean.

    Accepts 'y', 'yes', 'n', 'no' (case-insensitive).

    Args:
        prompt (str): The question to display to the user.

    Returns:
        bool: True if the answer was yes, False if no.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please answer with 'y' or 'n'.")


def main() -> None:
    """Run the password generator CLI."""
    print("Password Generator")
    # Prompt the user for a valid password length.
    while True:
        length_input = input("Enter the desired password length (positive integer): ")
        try:
            length = int(length_input)
            if length <= 0:
                print("Please enter a positive integer greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    # Ask the user which character sets to include.
    include_uppercase = ask_yes_no("Include uppercase letters? (y/n): ")
    include_lowercase = ask_yes_no("Include lowercase letters? (y/n): ")
    include_digits = ask_yes_no("Include digits? (y/n): ")
    include_symbols = ask_yes_no("Include symbols? (y/n): ")

    try:
        password = generate_password(
            length,
            use_uppercase=include_uppercase,
            use_lowercase=include_lowercase,
            use_digits=include_digits,
            use_symbols=include_symbols,
        )
        print(f"Generated password: {password}")
    except ValueError as exc:
        print(f"Error: {exc}")
        print(
            "Unable to generate password with the selected options."
        )


if __name__ == '__main__':
    main()