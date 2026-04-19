# auth.py
# Handles user login asks for username and password,
# checks them against saved data, and returns the user's info
# if everything matches.

from modules import file_handler


def login():
    """
    Shows a login prompt and gives the user up to 3 tries.
    If they get it right, it returns their full user info as a dictionary.
    If all 3 tries fail, it returns None so the program knows to stop.
    """

    print("\n" + "=" * 50)
    print("STUDENT PROFILE MANAGEMENT SYSTEM")
    print("=" * 50)

    # Load all saved passwords into a dictionary once
    # so we don't re-read the file on every attempt
    saved_passwords = file_handler.load_all_passwords()

    total_allowed_attempts = 3
    current_attempt        = 0

    while current_attempt < total_allowed_attempts:
        current_attempt = current_attempt + 1

        print("\n  Login Attempt " + str(current_attempt) + " of " + str(total_allowed_attempts))
        print("  " + "-" * 30)

        # Ask the user to type in their credentials
        entered_username = input("Username: ").strip()
        entered_password = input("Password: ").strip()

        # Check 1: Does this username exist in our password list?
        if entered_username not in saved_passwords:
            print("Username not found. Please try again.")
            continue   # skip to the next loop iteration (try again)

        # Check 2: Does the password match what we have saved?
        if saved_passwords[entered_username] != entered_password:
            print("Wrong password. Please try again.")
            continue

        # If we get here, both username and password are correct!
        # Load the full user profile and return it
        logged_in_user = file_handler.find_user_by_username(entered_username)
        print("\nWelcome, " + logged_in_user["name"] + "!")
        print("Role: " + logged_in_user["role"].upper())
        return logged_in_user

    # The loop finished without a successful login too many attempts
    print("\nToo many failed attempts. Exiting.")
    return None
