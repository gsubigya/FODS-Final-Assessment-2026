
# admin.py
# Everything the admin user can do:
# Add, view, modify, and delete student records
# View system-wide insights like averages and failing students

from modules import file_handler
from modules.student import Student


#  SMALL HELPER FUNCTIONS
#  These are reused in several places below.

def print_section_title(title=""):
    """Prints a divider line. If a title is given, shows it nicely."""
    if title == "":
        print("  " + "-" * 48)
    else:
        print("\n  --- " + title + " ---")


def ask_until_not_empty(prompt_text):
    """
    Keeps asking the user to type something until they actually type something.
    Prevents blank inputs for important fields.
    """
    while True:
        user_input = input(prompt_text).strip()
        if user_input != "":
            return user_input
        print("This field cannot be empty. Please type something.")


def ask_for_number(prompt_text, lowest=0, highest=100):
    """
    Keeps asking until the user types a valid whole number within the given range.
    Useful for scores and hours where we need a proper number.
    """
    while True:
        try:
            typed_number = int(input(prompt_text).strip())
            if lowest <= typed_number <= highest:
                return typed_number
            else:
                print("Please enter a number between " + str(lowest) + " and " + str(highest) + ".")
        except ValueError:
            print("That's not a valid number. Try again.")


#  1. ADD NEW USER

def add_new_user():
    """
    Guides the admin through creating a new user step by step.
    Saves the user to users.txt and passwords.txt.
    If the new user is a student, optionally adds grades and ECA too.
    """
    print_section_title("ADD NEW USER")

    # Keep asking until we get a username that isn't already taken
    while True:
        new_username = ask_until_not_empty("  Username: ")
        existing_user = file_handler.find_user_by_username(new_username)
        if existing_user is not None:
            print("That username is already taken. Please choose another.")
        else:
            break   # username is available, we can move on

    # Collect the rest of the basic info
    new_full_name  = ask_until_not_empty("  Full Name: ")
    new_email      = ask_until_not_empty("  Email: ")
    new_dob        = ask_until_not_empty("  Date of Birth (YYYY-MM-DD): ")
    new_password   = ask_until_not_empty("  Password: ")

    # Ask for role — must be exactly "admin" or "student"
    chosen_role = ""
    while chosen_role not in ("admin", "student"):
        chosen_role = input("  Role (admin / student): ").strip().lower()

    # Auto-generate the next available ID like U007
    generated_id = file_handler.make_new_user_id()

    # Build the user dictionary to save
    new_user_data = {
        "id":       generated_id,
        "username": new_username,
        "name":     new_full_name,
        "email":    new_email,
        "role":     chosen_role,
        "dob":      new_dob
    }

    # Save to files
    file_handler.add_new_user_to_file(new_user_data)
    file_handler.save_one_password(new_username, new_password)

    print("  [OK] User '" + new_username + "' created with ID " + generated_id)

    # If the new user is a student, offer to enter grades and ECA now
    if chosen_role == "student":
        want_grades = input("  Add grades now? (y/n): ").strip().lower()
        if want_grades == "y":
            collect_subject_grades(new_username)

        want_eca = input("  Add ECA activities now? (y/n): ").strip().lower()
        if want_eca == "y":
            collect_eca_activities(new_username)


def collect_subject_grades(username):
    """Asks the admin to enter a score for each of the 5 fixed subjects."""
    print("  Enter marks for each subject (0-100):")

    list_of_subjects = ["Math", "Science", "English", "Nepali", "Computer"]
    entered_grades   = {}

    for subject_name in list_of_subjects:
        score = ask_for_number("    " + subject_name + ": ", 0, 100)
        entered_grades[subject_name] = score

    file_handler.save_grades_for_student(username, entered_grades)
    print("  [OK] Grades saved.")


def collect_eca_activities(username):
    """Asks admin to enter ECA activities one by one. Type 'done' to stop."""
    print("  Enter ECA activities one at a time. Type 'done' when finished.")

    entered_activities = {}

    while True:
        activity_name = input("    Activity name (or 'done'): ").strip()

        if activity_name.lower() == "done":
            break

        if activity_name == "":
            continue   # skip if they pressed enter without typing anything

        hours_spent = ask_for_number("    Hours for " + activity_name + ": ", 0, 999)
        entered_activities[activity_name] = hours_spent

    if len(entered_activities) > 0:
        file_handler.save_eca_for_student(username, entered_activities)
        print("  [OK] ECA activities saved.")


#  2. VIEW ALL USERS

def view_all_users():
    """Prints a neatly formatted table of every user in the system."""
    print_section_title("ALL USERS")

    all_users = file_handler.load_all_users()

    if len(all_users) == 0:
        print("  No users found in the system.")
        return

    # Print the table header row
    print("  {:<6} {:<15} {:<20} {:<10} {}".format(
        "ID", "Username", "Name", "Role", "Email"))
    print_section_title()

    # Print one row per user
    for one_user in all_users:
        print("  {:<6} {:<15} {:<20} {:<10} {}".format(
            one_user["id"],
            one_user["username"],
            one_user["name"],
            one_user["role"],
            one_user["email"]
        ))


#  3. MODIFY STUDENT RECORD

def modify_student_record():
    """
    Lets the admin choose a student and then update their
    personal info, grades, or ECA activities.
    """
    print_section_title("MODIFY STUDENT RECORD")

    target_username = ask_until_not_empty("  Enter username to modify: ")
    found_user      = file_handler.find_user_by_username(target_username)

    if found_user is None:
        print("No user found with username '" + target_username + "'.")
        return

    # Show current details before asking what to change
    print("  Current info:")
    print("    Name  : " + found_user["name"])
    print("    Email : " + found_user["email"])
    print("    DOB   : " + found_user["dob"])

    print("\n  What would you like to modify?")
    print("  [1] Personal Info (name, email, DOB)")
    print("  [2] Grades")
    print("  [3] ECA Activities")

    admin_choice = input("Choice: ").strip()

    if admin_choice == "1":
        # Let admin change personal info pressing Enter keeps the old value
        new_name  = input("  New name  (Enter to keep current): ").strip()
        new_email = input("  New email (Enter to keep current): ").strip()
        new_dob   = input("  New DOB   (Enter to keep current): ").strip()

        # Only update the fields where the admin actually typed something
        if new_name  != "": found_user["name"]  = new_name
        if new_email != "": found_user["email"] = new_email
        if new_dob   != "": found_user["dob"]   = new_dob

        file_handler.update_existing_user(target_username, found_user)
        print("Personal info updated successfully.")

    elif admin_choice == "2":
        collect_subject_grades(target_username)

    elif admin_choice == "3":
        collect_eca_activities(target_username)

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")


# 4. DELETE STUDENT RECORD

def delete_student_record():
    """
    Permanently removes a user and all their data from the system.
    Asks for confirmation before deleting anything.
    """
    print_section_title("DELETE STUDENT RECORD")

    target_username = ask_until_not_empty("  Enter username to delete: ")
    found_user      = file_handler.find_user_by_username(target_username)

    if found_user is None:
        print("No user found with username '" + target_username + "'.")
        return

    # Ask the admin to confirm this is permanent!
    confirmation = input("Are you sure you want to permanently delete '" + target_username + "'? (yes/no): ").strip()

    if confirmation.lower() != "yes":
        print("Deletion cancelled. Nothing was changed.")
        return

    # Remove the user from all four data files
    file_handler.remove_user_by_username(target_username)
    file_handler.remove_one_password(target_username)
    file_handler.remove_grades_for_student(target_username)
    file_handler.remove_eca_for_student(target_username)

    print("User '" + target_username + "' and all their data have been deleted.")


#  5. SYSTEM INSIGHTS

def show_system_insights():
    """
    Analyses all students and shows useful statistics:
    Average grade per subject
    Most active ECA students
    Students who are failing
    The top performing student overall
    """
    print_section_title("Overview")

    # Load all users and filter down to students only
    all_users    = file_handler.load_all_users()
    student_list = []

    for one_user in all_users:
        if one_user["role"] == "student":
            student_object = Student(
                one_user["id"],
                one_user["username"],
                one_user["name"],
                one_user["email"],
                one_user["dob"]
            )
            student_list.append(student_object)

    if len(student_list) == 0:
        print("No students found in the system.")
        return

    #Average grade per subject across all students
    print("\nAverage Grade Per Subject:")
    subject_score_lists = {}   # will hold {subject: [all scores for that subject]}

    for each_student in student_list:
        for subject_name, score_value in each_student.grades.items():
            if subject_name not in subject_score_lists:
                subject_score_lists[subject_name] = []
            subject_score_lists[subject_name].append(score_value)

    for subject_name, score_list in subject_score_lists.items():
        class_average = round(sum(score_list) / len(score_list), 1)
        print("    " + subject_name + ": " + str(class_average) + "%")

    # Top 5 most active ECA students
    print("\nMost Active ECA Students (by total hours):")

    # Sort students by total ECA hours highest first
    # Using a simple bubble-style swap approach
    for i in range(len(student_list) - 1):
        for j in range(i + 1, len(student_list)):
            if student_list[j].get_total_eca_hours() > student_list[i].get_total_eca_hours():
                student_list[i], student_list[j] = student_list[j], student_list[i]

    for each_student in student_list[:5]:   # only show top 5
        total_hours    = each_student.get_total_eca_hours()
        activity_count = len(each_student.eca)
        print("    " + each_student.name + " - " + str(total_hours) + " hrs across " + str(activity_count) + " activities")

    # Students who are failing (below 60%)
    print("\nStudents Below 60% Average:")
    found_any_failing = False

    for each_student in student_list:
        if each_student.is_failing():
            found_any_failing = True
            print("    " + each_student.name + "  Avg: " + str(each_student.get_average()) + "% [" + each_student.get_grade_letter() + "]")

    if not found_any_failing:
        print("Great news, all students are currently passing!")

    # Find the top performer
    top_student = student_list[0]
    for each_student in student_list:
        if each_student.get_average() > top_student.get_average():
            top_student = each_student

    print("\nTop Performer: " + top_student.name + " with an average of " + str(top_student.get_average()) + "%")

# ADMIN MAIN MENU

def admin_menu(current_user):
    """
    The main menu loop for admin users.
    Keeps showing options until the admin chooses to logout.
    """
    while True:
        print("\n" + "=" * 50)
        print("ADMIN PANEL : " + current_user["name"])
        print("=" * 50)
        print("[1] Add New User")
        print("[2] View All Users")
        print("[3] Modify Student Record")
        print("[4] Delete Student Record")
        print("[5] System Insights")
        print("[6] Analytics Dashboard")
        print("[7] Logout")
        print("-" * 50)

        admin_choice = input("Enter choice: ").strip()

        if admin_choice == "1":
            add_new_user()

        elif admin_choice == "2":
            view_all_users()

        elif admin_choice == "3":
            modify_student_record()

        elif admin_choice == "4":
            delete_student_record()

        elif admin_choice == "5":
            show_system_insights()

        elif admin_choice == "6":
            # Only import analytics when the admin actually uses it
            from modules import analytics
            analytics.dashboard_menu()

        elif admin_choice == "7":
            print("\nLogged out successfully.\n")
            break   # exit the loop this logs the admin out

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")
