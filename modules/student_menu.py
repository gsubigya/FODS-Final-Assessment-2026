# student_menu.py
# Everything a student can do after logging in:
#   - View their profile, grades, and ECA
#   - Update personal info and change password
# Students can only see and change THEIR OWN data.

from modules import file_handler
from modules.student import Student #importing class Student from student.py


#  SMALL HELPER FUNCTIONS

def print_section_title(title=""):
    """Prints a divider line with an optional section title."""
    if title == "":
        print("  " + "-" * 48)
    else:
        print("\n  # " + title + " #")


def ask_until_not_empty(prompt_text):
    """Keeps asking the user to type something until they do."""
    while True:
        user_input = input(prompt_text).strip()
        if user_input != "":
            return user_input
        print("This field cannot be empty.")


#  1. VIEW FULL PROFILE
def view_profile(student_object):
    """Shows the student's full profile using the Student class method."""
    student_object.display_profile()


#  2. VIEW GRADES
def view_grades(student_object):
    """
    Shows each subject with its score, a simple bar chart made from #,
    and whether it's a pass or fail.
    Also shows the overall average and letter grade at the bottom.
    """
    print_section_title("GRADES")

    if len(student_object.grades) == 0:
        print("No grades have been recorded yet.")
        return

    # Print column headers
    print("  {:<15} {:>6}   {}".format("Subject", "Score", "Bar"))
    print_section_title()

    for subject_name, score_value in student_object.grades.items():
        # Build a simple ASCII bar — 1 block per 5 marks
        bar_visual = "#" * int(score_value / 5)

        # Show PASS or FAIL status next to the score
        if score_value >= 60:
            pass_fail_label = "[PASS]"
        else:
            pass_fail_label = "[FAIL]"

        print("  {:<15} {:>5}%  {}  {}".format(subject_name, score_value, pass_fail_label, bar_visual))

    print_section_title()
    print("Overall Average : " + str(student_object.get_average()) + "%")
    print("Letter Grade    : " + student_object.get_grade_letter())

    # Warn the student if their average is below the pass mark
    if student_object.is_failing():
        print("\n WARNING: Your average is below 60%. You are currently failing.")
    else:
        print("\n You are passing. Keep up the good work!")


#  3. VIEW ECA ACTIVITIES

def view_eca(student_object):
    """Shows all the student's ECA activities and their total hours."""
    print_section_title("MY ECA ACTIVITIES")

    if len(student_object.eca) == 0:
        print("No ECA activities have been recorded yet.")
        return

    print("  {:<25} {:>8}".format("Activity", "Hours"))
    print_section_title()

    for activity_name, hour_count in student_object.eca.items():
        print("  {:<25} {:>7} hrs".format(activity_name, hour_count))

    print_section_title()
    print("Total ECA Hours  :", student_object.get_total_eca_hours())
    print("Total Activities :", len(student_object.eca))


#  4. UPDATE PERSONAL INFO
def update_personal_info(student_object):
    """
    Lets the student update their own name, email, or date of birth.
    If they just press Enter, the current value is kept unchanged.
    """
    print_section_title("UPDATE MY INFO")
    print("  (Press Enter on any field to keep the current value)\n")

    # Show current values and ask for new ones
    print("Current Name: " + student_object.name)
    typed_name = input("New Name      : ").strip()

    print("Current Email: " + student_object.email)
    typed_email = input("New Email     : ").strip()

    print("Current DOB: " + student_object.dob)
    typed_dob = input("New DOB       : ").strip()

    # Load the full user record from the file
    user_record = file_handler.find_user_by_username(student_object.username)

    # Only update fields where the student actually typed something new
    if typed_name  != "": user_record["name"]  = typed_name
    if typed_email != "": user_record["email"] = typed_email
    if typed_dob   != "": user_record["dob"]   = typed_dob

    # Save the updated record back to the file
    file_handler.update_existing_user(student_object.username, user_record)
    print("Your profile has been updated successfully.")

    # Return the updated user dict so the menu can refresh the student object
    return user_record


#  5. CHANGE PASSWORD

def change_password(username):
    """
    Lets the student set a new password.
    They must first verify their current password before changing it.
    """
    print_section_title("CHANGE PASSWORD")

    all_passwords = file_handler.load_all_passwords()

    # Step 1: Confirm the current password
    entered_current = input("Current password : ").strip()
    if all_passwords[username] != entered_current:
        print("That's not the correct current password.")
        return

    # Step 2: Get the new password and confirm it
    new_password     = ask_until_not_empty("New password     : ")
    confirm_password = ask_until_not_empty("Confirm password : ")

    if new_password != confirm_password:
        print("Passwords don't match. Nothing was changed.")
        return

    # Step 3: Save the new password
    file_handler.save_one_password(username, new_password)
    print("Password changed successfully.")


#  STUDENT MAIN MENU

def student_menu(current_user):
    """
    The main menu loop for student users.
    Creates a Student object from the logged-in user's data,
    then shows options until the student logs out.
    """
    # Create the Student object for this user
    student_object = Student(
        current_user["id"],
        current_user["username"],
        current_user["name"],
        current_user["email"],
        current_user["dob"]
    )

    while True:
        print("\n" + "=" * 50)
        print("STUDENT PORTAL: " + student_object.name)
        print("=" * 50)
        print("[1] View Full Profile")
        print("[2] View My Grades")
        print("[3] View My ECA Activities")
        print("[4] Update Personal Info")
        print("[5] Change Password")
        print("[6] Logout")
        print("-" * 50)

        student_choice = input("Enter choice: ").strip()

        if student_choice == "1":
            view_profile(student_object)

        elif student_choice == "2":
            view_grades(student_object)

        elif student_choice == "3":
            view_eca(student_object)

        elif student_choice == "4":
            # After updating, reload the student object so changes show immediately
            updated_user = update_personal_info(student_object)
            student_object = Student(
                updated_user["id"],
                updated_user["username"],
                updated_user["name"],
                updated_user["email"],
                updated_user["dob"]
            )

        elif student_choice == "5":
            change_password(student_object.username)

        elif student_choice == "6":
            print("\nLogged out successfully.\n")
            break   # exit the loop this logs the student out

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")
