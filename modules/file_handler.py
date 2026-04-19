
# file_handler.py
# This file handles all reading and writing to our data files.
# Think of it like a mini-database manager using plain text files.
# Every other module uses these functions to get or save data.

import os


# File paths all data files live inside the "database" folder
DATA_FOLDER    = "database" #store this in same folder as main.py
USERS_FILE     = os.path.join(DATA_FOLDER, "users.txt")
PASSWORDS_FILE = os.path.join(DATA_FOLDER, "passwords.txt")
GRADES_FILE    = os.path.join(DATA_FOLDER, "grades.txt")
ECA_FILE       = os.path.join(DATA_FOLDER, "eca.txt")



#  HELPER FUNCTIONS
#  These are small utilities used by the bigger functions below.

def read_lines_from_file(file_path):
    """
    Opens a file and returns all non-empty lines as a list.
    If the file doesn't exist yet, it just returns an empty list
    instead of crashing the program.
    """
    all_lines = []

    try:
        opened_file = open(file_path, "r")
        for each_line in opened_file:
            clean_line = each_line.strip()   # remove spaces and newlines at both ends
            if clean_line != "":             # skip any blank lines
                all_lines.append(clean_line)
        opened_file.close()

    except FileNotFoundError:
        # File doesn't exist, just return nothing
        pass

    return all_lines


def write_lines_to_file(file_path, list_of_lines):
    """
    Writes a list of strings to a file, one string per line.
    This completely overwrites the old file content.
    """
    opened_file = open(file_path, "w")
    for each_line in list_of_lines:
        opened_file.write(each_line + "\n")
    opened_file.close()



#  PASSWORDS FILE
#  Each line looks like: username,password

def load_all_passwords():
    """
    Reads the passwords file and returns a dictionary.
    Example result: {"saksham": "subigya", "admin": "admin123"}
    """
    password_dict = {}

    for line in read_lines_from_file(PASSWORDS_FILE):
        parts    = line.split(",")   # split by comma
        username = parts[0]
        password = parts[1]
        password_dict[username] = password

    return password_dict


def save_one_password(username, new_password):
    """Adds a new password or updates an existing one, then saves."""
    password_dict = load_all_passwords()
    password_dict[username] = new_password   # add or overwrite

    # Rebuild the file content
    lines_to_write = []
    for user, pwd in password_dict.items():
        lines_to_write.append(user + "," + pwd)

    write_lines_to_file(PASSWORDS_FILE, lines_to_write)


def remove_one_password(username):
    """Deletes a user's password entry from the file."""
    password_dict = load_all_passwords()

    if username in password_dict:
        del password_dict[username]

    lines_to_write = []
    for user, pwd in password_dict.items():
        lines_to_write.append(user + "," + pwd)

    write_lines_to_file(PASSWORDS_FILE, lines_to_write)

#  USERS FILE
#  Each line: UserID,username,Full Name,email,role,date_of_birth
#  Example:   U002,saksham,Saksham Poudel,saksham@school.com,student,2003-05-12

def load_all_users():
    """
    Reads the users file and returns a list of dictionaries.
    Each dictionary is one user with keys: id, username, name, email, role, dob
    """
    user_list = []

    for line in read_lines_from_file(USERS_FILE):
        parts = line.split(",")

        # Build a dictionary for this user from each comma-separated field
        one_user = {
            "id":       parts[0],
            "username": parts[1],
            "name":     parts[2],
            "email":    parts[3],
            "role":     parts[4],
            "dob":      parts[5]
        }
        user_list.append(one_user)

    return user_list


def save_all_users(user_list):
    """
    Takes a list of user dictionaries and writes them back to the users file.
    Called after any add, update, or delete operation.
    """
    lines_to_write = []

    for one_user in user_list:
        # Join each field with a comma separator
        line = (one_user["id"]       + "," +
                one_user["username"] + "," +
                one_user["name"]     + "," +
                one_user["email"]    + "," +
                one_user["role"]     + "," +
                one_user["dob"])
        lines_to_write.append(line)

    write_lines_to_file(USERS_FILE, lines_to_write)


def find_user_by_username(username):
    """
    Searches through all users and returns the one matching the username.
    Returns None if the user is not found.
    """
    for one_user in load_all_users():
        if one_user["username"] == username:
            return one_user

    return None   # not found


def add_new_user_to_file(new_user_dict):
    """Adds a new user dictionary to the list and saves the file."""
    user_list = load_all_users()
    user_list.append(new_user_dict)
    save_all_users(user_list)


def update_existing_user(username, updated_user_dict):
    """
    Finds the user matching the given username and replaces their data.
    Returns True if successful, False if username not found.
    """
    user_list = load_all_users()

    for index in range(len(user_list)):
        if user_list[index]["username"] == username:
            user_list[index] = updated_user_dict   # replace with new data
            save_all_users(user_list)
            return True

    return False   # user was not found


def remove_user_by_username(username):
    """Removes a user from the list by their username and saves."""
    user_list    = load_all_users()
    updated_list = []

    for one_user in user_list:
        if one_user["username"] != username:
            updated_list.append(one_user)   # keep everyone except the target

    save_all_users(updated_list)


def make_new_user_id():
    """
    Looks at the highest existing user ID and returns the next one.
    For example, if the highest is U004, this returns U005.
    Used U here to indicate User.
    """
    user_list = load_all_users()

    if len(user_list) == 0:
        return "U001"   # very first user ever

    # Find the largest ID number currently in the file
    highest_number = 0
    for one_user in user_list:
        # The ID looks like "U003" — slice off the "U" and convert to int
        id_number = int(one_user["id"][1:])
        if id_number > highest_number:
            highest_number = id_number

    # Increment by 1 and pad to 3 digits (e.g. 5 becomes "005")
    next_number = highest_number + 1
    return "U" + str(next_number).zfill(3)



#  GRADES FILE
#  Each line: username,Subject:Score,Subject:Score,...
#  Example:   saksham,Math:78,Science:85,English:72

def load_all_grades():
    """
    Reads grades file and returns a dictionary of dictionaries.
    Example: {"saksham": {"Math": 78, "Science": 85, ...}}
    """
    grades_for_all = {}

    for line in read_lines_from_file(GRADES_FILE):
        parts    = line.split(",")
        username = parts[0]

        # Parse each "Subject:Score" pair (skip the username at index 0)
        subject_score_dict = {}
        for entry in parts[1:]:
            subject_and_score = entry.split(":")
            subject_name      = subject_and_score[0]
            score_number      = int(subject_and_score[1])
            subject_score_dict[subject_name] = score_number

        grades_for_all[username] = subject_score_dict

    return grades_for_all


def save_all_grades(grades_for_all):
    """Writes the full grades dictionary back to the grades file."""
    lines_to_write = []

    for username, subject_score_dict in grades_for_all.items():
        # Start with the username, then append each "Subject:Score"
        row_parts = [username]
        for subject_name, score_number in subject_score_dict.items():
            row_parts.append(subject_name + ":" + str(score_number))
        lines_to_write.append(",".join(row_parts))

    write_lines_to_file(GRADES_FILE, lines_to_write)


def get_grades_for_student(username):
    """Returns the grade dictionary for one student. Empty dict if none found."""
    all_grades = load_all_grades()

    if username in all_grades:
        return all_grades[username]

    return {}   # student has no grades yet


def save_grades_for_student(username, grade_dict):
    """Saves or replaces grades for a single student."""
    all_grades = load_all_grades()
    all_grades[username] = grade_dict
    save_all_grades(all_grades)


def remove_grades_for_student(username):
    """Deletes all grade records for a student."""
    all_grades = load_all_grades()

    if username in all_grades:
        del all_grades[username]

    save_all_grades(all_grades)



#  ECA FILE
#  Each line: username,Activity:Hours,Activity:Hours,...
#  Example:   saksham,Football:3,Debate Club:2,Photography:1

def load_all_eca():
    """
    Reads ECA file and returns a dictionary of dictionaries.
    Example: {"saksham": {"Football": 3, "Debate Club": 2}}
    """
    eca_for_all = {}

    for line in read_lines_from_file(ECA_FILE):
        parts    = line.split(",")
        username = parts[0]

        # Parse each "Activity:Hours" pair
        activity_dict = {}
        for entry in parts[1:]:
            activity_and_hours = entry.split(":")
            activity_name      = activity_and_hours[0]
            hours_count        = int(activity_and_hours[1])
            activity_dict[activity_name] = hours_count

        eca_for_all[username] = activity_dict

    return eca_for_all


def save_all_eca(eca_for_all):
    """Writes the full ECA dictionary back to the ECA file."""
    lines_to_write = []

    for username, activity_dict in eca_for_all.items():
        row_parts = [username]
        for activity_name, hours_count in activity_dict.items():
            row_parts.append(activity_name + ":" + str(hours_count))
        lines_to_write.append(",".join(row_parts))

    write_lines_to_file(ECA_FILE, lines_to_write)


def get_eca_for_student(username):
    """Returns ECA activity dictionary for one student. Empty dict if none."""
    all_eca = load_all_eca()

    if username in all_eca:
        return all_eca[username]

    return {}


def save_eca_for_student(username, activity_dict):
    """Saves or replaces ECA activities for one student."""
    all_eca = load_all_eca()
    all_eca[username] = activity_dict
    save_all_eca(all_eca)


def remove_eca_for_student(username):
    """Deletes all ECA records for a student."""
    all_eca = load_all_eca()

    if username in all_eca:
        del all_eca[username]

    save_all_eca(all_eca)
