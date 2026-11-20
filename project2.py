
import string

COMMON_PASSWORDS = {
    "password",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "password123",
    "123456789",
}


def check_password(password):
    feedback = []
    score = 0

    if not password:
        return 0, ["Password cannot be empty."]

    if password.lower() in COMMON_PASSWORDS:
        return 0, [
            "This password is very common. Choose a different one."
        ]

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add special characters.")

    if len(password) >= 16:
        score += 1

    return score, feedback


def get_strength(score):
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    elif score <= 5:
        return "Strong"
    return "Very Strong"


def main():
    print("=" * 40)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 40)

    while True:
        password = input(
            "\nEnter a password (or type 'exit'): "
        )

        if password.lower() == "exit":
            print("Goodbye!")
            break

        score, feedback = check_password(password)

        if not password:
            print("Please enter a password.")
            continue

        print("\nPassword Strength:", get_strength(score))
        print("Score:", score, "/ 7")

        if feedback:
            print("\nSuggestions:")
            for item in feedback:
                print("-", item)
        else:
            print("\nYour password meets all basic checks!")


if __name__ == "__main__":
    main()
