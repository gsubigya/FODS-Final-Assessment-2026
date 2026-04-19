# student.py
# Defines the Student class using Object-Oriented Programming.
# When you create a Student object, it automatically loads that
# student's grades and ECA data from the files.

from modules import file_handler


class Student:
    """
    Represents a single student in the system.
    Holds all personal info, grades, and ECA activities.

    Attributes:
      student_id  : e.g. "U002", "U for User"
      username    : e.g. "saksham"
      name        : e.g. "Saksham Poudel"
      email       : e.g. "saksham@school.com"
      dob         : e.g. "2003-05-12"
      grades      : dictionary like {"Math": 78, "Science": 85}
      eca         : dictionary like {"Football": 3, "Debate Club": 2}
    """

    def __init__(self, student_id, username, full_name, email_address, date_of_birth):
        """
        Constructor runs when we create a new Student object.
        Saves the basic info and automatically loads grades and ECA.
        """
        # Store the basic personal info
        self.student_id = student_id
        self.username = username
        self.name = full_name
        self.email = email_address
        self.dob = date_of_birth

        # Load grades and ECA from file automatically
        self.grades = file_handler.get_grades_for_student(username)
        self.eca = file_handler.get_eca_for_student(username)


    #  Grade Calculation Methods

    def get_average(self):
        """
        Calculates the average score across all subjects.
        Returns 0 if the student has no grades recorded yet.
        """
        if len(self.grades) == 0:
            return 0

        total_score = 0
        for each_score in self.grades.values():
            total_score = total_score + each_score

        average_score = total_score / len(self.grades)
        return round(average_score, 2)   # round to 2 decimal places

    def get_grade_letter(self):
        """
        Converts the numeric average into a letter grade.
        A+ is 90 and above, and it goes down from there.
        """
        average = self.get_average()

        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B+"
        elif average >= 60:
            return "B"
        elif average >= 50:
            return "C"
        else:
            return "F"

    def is_failing(self):
        """Returns True if the student's average is below 60 (the pass mark)."""
        return self.get_average() < 60


    #  ECA Methods

    def get_total_eca_hours(self):
        """Adds up all the hours across every ECA activity and returns the total."""
        total_hours = 0
        for each_hour_count in self.eca.values():
            total_hours = total_hours + each_hour_count
        return total_hours
    
    #  Display Method

    def display_profile(self):
        """Prints all the student's information in a clean, readable format."""
        print("\n ---> STUDENT PROFILE <---")
        print("ID       :", self.student_id)
        print("Username :", self.username)
        print("Name     :", self.name)
        print("Email    :", self.email)
        print("DOB      :", self.dob)

        # Show grades section
        if len(self.grades) == 0:
            print("Grades: No grades recorded yet")
        else:
            print("Grades:")
            for subject_name, score_value in self.grades.items():
                print("  " + subject_name + ": " + str(score_value))
            print("Average:", self.get_average(), "(" + self.get_grade_letter() + ")")

        # Show ECA section
        if len(self.eca) == 0:
            print("ECA: No activities recorded yet")
        else:
            print("ECA:")
            for activity_name, hour_count in self.eca.items():
                print("  " + activity_name + ": " + str(hour_count) + " hrs")
            print("ECA Total:", self.get_total_eca_hours(), "hours")
