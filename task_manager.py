# Task Manager

# Capstone task 17

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if ';' in user:
        username, password = user.split(';', 1)
        username_password[username] = password

# Add a new user to the user.txt file'''
def reg_user():
    # Input new username
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please try a different username.")
        return
    # Input new password and confirmation
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # Checks username and password
    if new_password == confirm_password:
        # Adds to .txt file if they match
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            for k, v in username_password.items():
                out_file.write(f"{k};{v}\n")
    # Otherwise a relevant message displays
    else:
        print("Passwords do not match")

'''User input a new task to .txt file with:
    - Username with the assignee
    - Task title
    - Task description
    - Task due date'''
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    # Adds data to the .txt file with 'No' if the task is complete

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            task_file.write(f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime(DATETIME_STRING_FORMAT)};{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if t['completed'] else 'No'}\n")
    print("Task successfully added.")

def view_all():

    # Reads task.txt file and prints to the console

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\nAssigned to: \t {t['username']}\nDate Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\nDue Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\nTask Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(curr_user):
    # Reads task from .txt file and prints output.
    
    user_tasks = [t for t in task_list if t['username'] == curr_user]

    if not user_tasks:
        print("You don't have any tasks assigned.")
        return

    for idx, t in enumerate(user_tasks, start=1):
        disp_str = f"Task {idx}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: {t['description']}\n"
        disp_str += f"Completed: {t['completed']}\n"
        print(disp_str)

    task_choice = input("Enter the number of the task you want to select, or '-1' to return to the main menu: ")
    try:
        task_choice = int(task_choice)
        if task_choice == -1:
            return
        elif 1 <= task_choice <= len(user_tasks):
            selected_task = user_tasks[task_choice - 1]
            task_action(selected_task)
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# User input to mark a task as complete or to make an edit
        
def task_action(task):
    print("1. Mark the task as complete")
    print("2. Edit the task")
    action = input("Select an option: ")
    if action == '1':
        mark_task_as_complete(task)
    elif action == '2':
        edit_task(task)
    else:
        print("Invalid option.")

# Marks the file as complete
        
def mark_task_as_complete(task):
    task['completed'] = True
    update_tasks_file()

# User input to edit the task
    
def edit_task(task):
    if task['completed']:
        print("Completed tasks cannot be edited.")
        return
    
    new_username = input("Enter new username (leave blank to keep current): ")
    if new_username:
        if new_username in username_password.keys():
            task['username'] = new_username

        else:
            print("Username does not exist. Keeping the current assignment.")
    new_due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ")
    if new_due_date:
        try:
            task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid date format. Keeping the current due date.")
    update_tasks_file()

# Amends task file in the folder
    
def update_tasks_file():

    with open("tasks.txt", "w") as task_file:

        for task in task_list:
            task_str = f"{task['username']};{task['title']};{task['description']};"
            task_str += f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
            task_str += f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
            task_str += "Yes" if task['completed'] else "No"
            task_file.write(task_str + "\n")

def generate_reports():
    '''Calculates the statistics and then creates reports as .txt files 
    and saves them in the same folder or updates the report if it's 
    already generated.'''

    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks

    today_datetime = datetime.combine(date.today(), datetime.min.time())

    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < today_datetime)

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    # Write task_overview.txt with the calculations required
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Incomplete Percentage: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Overdue Percentage: {overdue_percentage:.2f}%\n")

    # Write task_overview.txt with the calculations required
    total_users = len(username_password)
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total Users: {total_users}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")

        for username, password in username_password.items():
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            uncompleted_user_tasks = total_user_tasks - completed_user_tasks

            today_datetime = datetime.combine(date.today(), datetime.min.time())
            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'] < today_datetime)

            user_percentage = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            completed_user_percentage = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            uncompleted_user_percentage = (uncompleted_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            overdue_user_percentage = (overdue_user_tasks / uncompleted_user_tasks) * 100 if uncompleted_user_tasks > 0 else 0

            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total User Tasks: {total_user_tasks}\n")
            user_overview_file.write(f"User Percentage: {user_percentage:.2f}%\n")
            user_overview_file.write(f"Completed User Tasks: {completed_user_tasks}\n")
            user_overview_file.write(f"Completed User Percentage: {completed_user_percentage:.2f}%\n")
            user_overview_file.write(f"Uncompleted User Tasks: {uncompleted_user_tasks}\n")
            user_overview_file.write(f"Uncompleted User Percentage: {uncompleted_user_percentage:.2f}%\n")
            user_overview_file.write(f"Overdue User Tasks: {overdue_user_tasks}\n")
            user_overview_file.write(f"Overdue User Percentage: {overdue_user_percentage:.2f}%\n")

    print("Reports generated successfully.")

def display_statistics():
    # If user is admin, allows a display of statistics on user and tasks

    generate_reports()
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("..........................................")
    with open("task_overview.txt", "r") as task_overview_file:
        print("\nTask Overview Report:\n" + task_overview_file.read())

    with open("user_overview.txt", "r") as user_overview_file:
        print("\nUser Overview Report:\n" + user_overview_file.read())
        print("..........................................")

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password:
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login Successful!")
        logged_in = True

while True:
# Menu shows to user
    print()
    menu = input('''Select one of the following Options below:
..........................................
r - register user
a - add task
va - view all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
..........................................
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(curr_user)
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports()
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice. Please try again.")
