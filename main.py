"""
main.py
The entry point for the Student Management System.
Run this file to start: python main.py

What happens when you run this:
1. A welcome banner is shown
2. The user logs in
3. The program checks if they're an admin or student
4. It opens the right menu based on their role
5. After they log out, it asks if another user wants to log in
"""

from modules import auth
from modules import admin
from modules import student_menu


def show_welcome_banner():
    """Prints the welcome banner when the program first starts."""
    print("\n" + "=" * 50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("FODS Final Project")
    print("=" * 50)
    print("Available Accounts (FOR DEMO):")
    print("Admin   = admin/admin123")
    print("Student = saksham/subigya")
    print("=" * 50)


def main():
    """
    The main function that runs the whole program.
    Uses a loop so multiple users can log in one after another.
    """
    show_welcome_banner()

    while True:
        # Step 1: Try to log in
        # auth.login() gives back the user dictionary if login works, or None if it fails
        logged_in_user = auth.login()

        # If login failed (None was returned), stop the program
        if logged_in_user is None:
            break

        # Step 2: Check the role and open the correct menu
        user_role = logged_in_user["role"]

        if user_role == "admin":
            # Admins go to the admin panel where they can manage everyone
            admin.admin_menu(logged_in_user)

        elif user_role == "student":
            # Students go to their own portal — they can only see their own data
            student_menu.student_menu(logged_in_user)

        else:
            # This shouldn't normally happen, but handled just in case
            print("Unknown role: " + user_role)

        # Step 3: After logout, ask if another person wants to log in
        try_again = input("Login with another account? (y/n): ").strip().lower()
        if try_again != "y":
            print("\n Thank you for using the system. Goodbye!\n")
            break


# Only run main() if this file is executed directly
# (not if it's imported by another file)
if __name__ == "__main__":
    main()
