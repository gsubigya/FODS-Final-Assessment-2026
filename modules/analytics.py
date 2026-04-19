
# analytics.py
# Performance Analytics Dashboard for admin users.
# Uses matplotlib for charts and pandas for statistics.
# Charts are saved as PNG files in the "charts" folder.

import os
from modules import file_handler
from modules.student import Student

# The folder where all chart images will be saved
CHARTS_SAVE_FOLDER = "charts"


#  LOAD ALL STUDENTS

def get_all_students_as_objects():
    """
    Reads all users, filters to role=student, and
    returns a list of Student objects ready to use.
    """
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

    return student_list


#  CHART 1 GRADE TRENDS
#  Bar chart showing each student's average grade

def chart_grade_trends(student_list):
    """
    Creates a bar chart showing each student's average grade.
    Green bars = passing, Red bars = failing.
    Saves to charts/grade.png
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed. Run: pip install matplotlib")
        return

    # Create the charts folder if it doesn't exist yet
    if not os.path.exists(CHARTS_SAVE_FOLDER):
        os.makedirs(CHARTS_SAVE_FOLDER)

    # Build the data lists for the chart
    first_name_list = []
    average_list    = []
    bar_colour_list = []

    for each_student in student_list:
        first_name_list.append(each_student.name.split()[0])   # first name only to save space
        student_average = each_student.get_average()
        average_list.append(student_average)

        # Choose bar colour based on whether they're passing or failing
        if student_average >= 60:
            bar_colour_list.append("green")
        else:
            bar_colour_list.append("red")

    # Create and configure the bar chart
    fig, chart_axes = plt.subplots(figsize=(8, 5))
    bar_objects = chart_axes.bar(first_name_list, average_list, color=bar_colour_list)

    # Add the score number label on top of each bar
    for one_bar, one_average in zip(bar_objects, average_list):
        chart_axes.text(
            one_bar.get_x() + one_bar.get_width() / 2,   # centre horizontally
            one_bar.get_height() + 1,                      # just above the bar
            str(one_average) + "%",
            ha="center", fontsize=10, fontweight="bold"
        )

    # Add a dashed orange line at the 60% pass threshold
    chart_axes.axhline(y=60, color="orange", linewidth=1.5,
                       linestyle="--", label="Pass Threshold (60%)")

    chart_axes.set_ylim(0, 110)
    chart_axes.set_title("Student Grade Trends", fontsize=14, fontweight="bold")
    chart_axes.set_xlabel("Students")
    chart_axes.set_ylabel("Average Grade (%)")
    chart_axes.legend()

    # Save and close the chart
    save_path = os.path.join(CHARTS_SAVE_FOLDER, "grade.png")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print("Chart saved: " + save_path)


#  CHART 2 ECA IMPACT
#  Scatter plot comparing ECA hours against average grade

def chart_eca_impact(student_list):
    """
    Creates a scatter plot to see if ECA hours affect grades.
    Each dot is one student, labelled with their first name.
    Saves to charts/eca_.png
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed.")
        return

    if not os.path.exists(CHARTS_SAVE_FOLDER):
        os.makedirs(CHARTS_SAVE_FOLDER)

    # Collect the data points
    eca_hour_list   = []
    average_list    = []
    first_name_list = []

    for each_student in student_list:
        eca_hour_list.append(each_student.get_total_eca_hours())
        average_list.append(each_student.get_average())
        first_name_list.append(each_student.name.split()[0])

    fig, chart_axes = plt.subplots(figsize=(8, 5))

    # Plot one dot per student
    chart_axes.scatter(eca_hour_list, average_list, color="steelblue", s=100, zorder=5)

    # Label each dot with the student's name
    for first_name, x_pos, y_pos in zip(first_name_list, eca_hour_list, average_list):
        chart_axes.annotate(first_name, (x_pos, y_pos),
                            textcoords="offset points", xytext=(5, 3), fontsize=9)

    chart_axes.set_title("ECA Hours vs Academic Performance", fontsize=14, fontweight="bold")
    chart_axes.set_xlabel("Total ECA Hours")
    chart_axes.set_ylabel("Average Grade (%)")
    chart_axes.set_ylim(0, 110)
    chart_axes.grid(True, linestyle="--", alpha=0.5)

    save_path = os.path.join(CHARTS_SAVE_FOLDER, "eca.png")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print("Chart saved: " + save_path)



#  CHART 3 — SUBJECT BREAKDOWN
#  Grouped bar chart with all students' scores per subject

def chart_subject_breakdown(student_list):
    """
    Shows every student's scores side by side for each subject.
    Makes it easy to spot who is strong or weak in which subject.
    Saves to charts/subject.png
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib and/or numpy not installed.")
        return

    if not os.path.exists(CHARTS_SAVE_FOLDER):
        os.makedirs(CHARTS_SAVE_FOLDER)

    # Collect all unique subject names across all students
    all_subjects = []
    for each_student in student_list:
        for subject_name in each_student.grades.keys():
            if subject_name not in all_subjects:
                all_subjects.append(subject_name)

    if len(all_subjects) == 0:
        print("No grade data available to chart.")
        return

    # Set up grouped bar positions
    x_positions = np.arange(len(all_subjects))   # one group per subject
    num_students = len(student_list)
    single_bar_width = 0.8 / num_students         # divide space evenly among students

    fig, chart_axes = plt.subplots(figsize=(10, 6))

    # Draw one set of bars per student
    for student_index, each_student in enumerate(student_list):
        # Get scores for each subject (0 if the student has no entry for that subject)
        score_list = []
        for subject_name in all_subjects:
            score_list.append(each_student.grades.get(subject_name, 0))

        offset = (student_index - num_students / 2 + 0.5) * single_bar_width
        chart_axes.bar(x_positions + offset, score_list, single_bar_width * 0.9,
                       label=each_student.name.split()[0])

    chart_axes.set_xticks(x_positions)
    chart_axes.set_xticklabels(all_subjects)
    chart_axes.set_title("Per-Subject Grade Breakdown", fontsize=14, fontweight="bold")
    chart_axes.set_xlabel("Subject")
    chart_axes.set_ylabel("Score (%)")
    chart_axes.set_ylim(0, 110)
    chart_axes.axhline(y=60, color="red", linestyle="--", linewidth=1, label="Pass (60%)")
    chart_axes.legend()
    chart_axes.grid(axis="y", linestyle="--", alpha=0.5)

    save_path = os.path.join(CHARTS_SAVE_FOLDER, "subject.png")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print("Chart saved: " + save_path)


#  PERFORMANCE ALERTS

def show_performance_alerts(student_list, passing_threshold=60):
    """
    Checks every student's average against the passing threshold.
    Lists failing students and suggests actions to help them.
    """
    print("\nPERFORMANCE ALERTS (Threshold: " + str(passing_threshold) + "%)")

    # Find all students who are below the threshold
    at_risk_list = []
    for each_student in student_list:
        if each_student.get_average() < passing_threshold:
            at_risk_list.append(each_student)

    if len(at_risk_list) == 0:
        print("All students are above " + str(passing_threshold) + "%. No alerts.")
        return

    print("  " + str(len(at_risk_list)) + " student(s) need attention:\n")

    for each_student in at_risk_list:
        student_average = each_student.get_average()

        print("Student: " + each_student.name)
        print("Average: " + str(student_average) + "% [" + each_student.get_grade_letter() + "]")

        # Find which specific subjects they're failing
        weak_subject_list = []
        for subject_name, score_value in each_student.grades.items():
            if score_value < passing_threshold:
                weak_subject_list.append(subject_name + " (" + str(score_value) + "%)")

        if len(weak_subject_list) > 0:
            print("Weak In  : " + ", ".join(weak_subject_list))

        # Suggest different actions depending on how serious the situation is
        print("Suggested Action:")
        if student_average < 40:
            print("Urgent: arrange one-on-one tutoring immediately")
            print("Notify parents or guardians")
        elif student_average < 50:
            print("Provide extra study materials for weak subjects")
            print("Schedule weekly check-ins with a teacher")
        else:
            print("Encourage joining a peer study group")
            print("Review past exam papers together")

        # If student is doing lots of ECA, suggest reducing it temporarily
        if each_student.get_total_eca_hours() > 15:
            print("Consider reducing ECA commitments temporarily")

        print()


#  PANDAS SUMMARY REPORT

def show_pandas_summary(student_list):
    """
    Uses the pandas library to create a summary table with statistics.
    Shows mean, min, max, and standard deviation for grades and ECA.
    Also shows the correlation between ECA hours and grade average.
    """
    print("\n PANDAS SUMMARY REPORT")

    try:
        import pandas as pd
    except ImportError:
        # If pandas isn't installed, show a simpler text table instead
        print("pandas not installed. Run: pip install pandas")
        print("\nBasic Summary (pandas not available):")
        print("  {:<20} {:>10} {:>12}".format("Name", "Average Grade", "ECA Hours"))
        print("  " + "-" * 44)
        for each_student in student_list:
            print("  {:<20} {:>9}% {:>12}".format(
                each_student.name,
                each_student.get_average(),
                each_student.get_total_eca_hours()
            ))
        return

    # Build a list of rows to turn into a DataFrame
    row_list = []
    for each_student in student_list:
        one_row = {
            "Name"      : each_student.name,
            "Username"  : each_student.username,
            "Average Grade" : each_student.get_average(),
            "ECA Hours" : each_student.get_total_eca_hours(),
            "Grade"     : each_student.get_grade_letter()
        }
        # Add each subject's score as its own column
        for subject_name, score_value in each_student.grades.items():
            one_row[subject_name] = score_value

        row_list.append(one_row)

    # Create the pandas DataFrame
    data_frame = pd.DataFrame(row_list)

    print("\n  All Students:")
    print(data_frame[["Name", "Average Grade", "ECA Hours", "Grade"]].to_string(index=False))

    print("\n  Statistics (numeric columns only):")
    numeric_columns = data_frame.select_dtypes(include="number")
    print(numeric_columns.describe().round(2).to_string())

    # Show how strongly ECA hours correlate with average grade
    if "Average Grade" in data_frame.columns and "ECA Hours" in data_frame.columns:
        correlation_value = data_frame["ECA Hours"].corr(data_frame["Average Grade"])
        print("\n  ECA Hours <-> Grade Correlation: " + str(round(correlation_value, 3)))

        if correlation_value > 0.5:
            print("Interpretation: Strong positive more ECA seems to help grades.")
        elif correlation_value < -0.5:
            print("Interpretation: Strong negative too much ECA may be hurting grades.")
        else:
            print("Interpretation: Weak ECA hours don't clearly affect grades either way.")


#  ANALYTICS DASHBOARD MENU
def dashboard_menu():
    """
    Admin submenu for the analytics dashboard.
    Loads all students once, then lets the admin pick what to view.
    """
    all_students = get_all_students_as_objects()

    if len(all_students) == 0:
        print("  No students found in the system.")
        return

    while True:
        print("\nANALYTICS DASHBOARD")
        print("[1] Grade Trends Chart")
        print("[2] ECA vs Grades Chart")
        print("[3] Subject Breakdown Chart")
        print("[4] Performance Alerts")
        print("[5] Pandas Summary Report")
        print("[6] Back to Admin Panel")

        dashboard_choice = input("  Choice: ").strip()

        if dashboard_choice == "1":
            chart_grade_trends(all_students)

        elif dashboard_choice == "2":
            chart_eca_impact(all_students)

        elif dashboard_choice == "3":
            chart_subject_breakdown(all_students)

        elif dashboard_choice == "4":
            show_performance_alerts(all_students)

        elif dashboard_choice == "5":
            show_pandas_summary(all_students)

        elif dashboard_choice == "6":
            break   # go back to admin menu

        else:
            print("Invalid choice. Enter 1-6.")
