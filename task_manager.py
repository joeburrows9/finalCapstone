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

# Date formatting 

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Reads task data
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Creates task list
 
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], 
                                           DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], 
                                                DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# Variables to be used later
    
total_tasks = len(task_list)
completed_tasks = sum(task['completed'] for task in task_list)
overdue_user_tasks = sum(1 for task in task_list if not task['completed'] 
                         and task['due_date'].date() < datetime.now().date())
incomplete_tasks = total_tasks - completed_tasks

# If statement calculates the percentage

if completed_tasks >= 1:
    percentage_incomplete = float((incomplete_tasks / total_tasks) * 100)
elif completed_tasks <= 1:
    percentage_incomplete = 100
else:
    print("")

overdue_tasks = sum(1 for task in task_list if not task['completed'] and 
                    task['due_date'].date() < datetime.now().date())

# If statement calculates the percentage

if overdue_tasks >= 1:
    percentage_overdue = float((overdue_tasks / total_tasks) * 100)
elif overdue_tasks <= 1:
    percentage_overdue = 0
else:
    print("")
reg_user = "r"
add_task = "a"
view_all = "va"
view_mine = "vm"
generate_reports = "gr"
display_statistics = "ds"


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# Some definitions to start

# If no user.txt file, create one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Load existing usernames
username_password = {}
try:
    with open("user.txt", "r") as in_file:
        for line in in_file:
            user, password = line.strip().split(';')
            username_password[user] = password
except FileNotFoundError:
    # If the file does not exist, proceed with an empty dictionary
    pass


# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if ';' in user:
        username, password = user.split(';', 1)
        username_password[username] = password
    else:
        print(f"Invalid entry: {user}")

# Login starts here

logged_in = False
while not logged_in:

    # Checks login credentials

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    # Register user

    # Add a new user to the user.txt file
    if menu == reg_user:
   
        # Load existing usernames
        username_password = {}
        try:
            with open("user.txt", "r") as in_file:
                for line in in_file:
                    user, password = line.strip().split(';')
                    username_password[user] = password
        except FileNotFoundError:
            # If the file does not exist, proceed with an empty dictionary
            pass

        # Request input of a new username
        new_username = input("New Username: ")

        # Check if the username already exists.
        if new_username in username_password:
            print("Error: Username already exists. Please try a different username.")
        else:
            # Request input of a new password.
            new_password = input("New Password: ")

            # Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # If they are the same, add them to the user.txt file.
                print("New user added")
                username_password[new_username] = new_password

                # Write all user data back to file.
                with open("user.txt", "w") as out_file:
                    for username, password in username_password.items():
                        out_file.write(f"{username};{password}\n")
            # Otherwise you display a relevant message.
            else:
                print("Error: Passwords do not match.")

    # Add task

    elif menu == add_task:
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
        # Add a name

        task_username = input("Name of person assigned to task: ")

        # Checks the user exists in txt file
        if task_username not in username_password:
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        # Due dates in the past are rejected
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                if due_date_time < datetime.now():
                    print("Due date cannot be set to a date in the past. Please enter a future date.")
                    continue
                else:
                    print("")
                break

            # Error message for incorrect data formatting
            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        # Updates the task in file

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


# View all

    elif menu == view_all:
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        # Shows the data with titles for how they appear in the txt file

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    # View mine       

    elif menu == view_mine:
        '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing and labeling)'''

        # Shows current task list out of those which are still active

        for i, t in enumerate(task_list, 1):
            if t['username'] == curr_user:
                disp_str = f"Task {i}:\n"
                disp_str += f"  Title: {t['title']}\n"
                disp_str += f"  Assigned to: {t['username']}\n"
                disp_str += f"  Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"  Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"  Task Description: {t['description']}\n"
                disp_str += f"  Completed: {t['completed']}\n"
                print(disp_str)

        # The user can select a task or return to the main menu.
                
        task_choice = input("Please enter the your task number, or enter -1 to return to the main menu: ")

        if task_choice.isdigit() and 1 <= int(task_choice) <= len(task_list):
            selected_task_index = int(task_choice) - 1
            selected_task = task_list[selected_task_index]

            # If it has been completed an error message displays

            if selected_task['completed']:
                print("Error: This task is already completed and cannot be edited.")
                continue

            # User option to mark complete or to edit the task.

            action_choice = input('''Please select an action:
                                  1. Mark as Complete
                                  2. Edit Task
                                  
                                  Enter your selection: ''')

            if action_choice == '1':

                # To mark a task as complete.

                selected_task['completed'] = True
                print("Task marked as complete.")
            
            elif action_choice == '2':

                # Edit the task only if not completed.

                new_username = input("Enter new username: ")

                # Checks the username exists.

                if new_username not in username_password:
                    print("User does not exist. Please enter a valid username")
                    continue
                else:
                    print("")

                # Checks date is in the future
                # Shows error if in the past
                    while True:
                        try:
                            new_due_date = input("Enter new due date of task (YYYY-MM-DD): ")
                            new_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            if new_date_time < datetime.now():
                                print("Due date cannot be set to a date in the past. Please enter a future date.")
                                continue
                            else:
                                print("")
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                # Continues to other questions
                if new_username:
                    selected_task['username'] = new_username

                if new_due_date:
                    selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)

                    print("Task edited successfully.")
                else:
                    print("")
            
            # Error messages for invalid input

            elif action_choice == '2' and selected_task['completed'] == 'Yes':
                print("Error: Unable to edit task.")

            else:
                print("Invalid input.")


        # After updating task_list with new_task or edited task
                
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))

# Generate reports

    elif menu == generate_reports: 

        print("\n\nYour report is generating - check your source folder!")

        # This path creates a task overview.

        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
            task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
            task_overview_file.write(f"Total number of incomplete tasks: {incomplete_tasks}\n")
            task_overview_file.write(f"Total number of tasks overdue: {overdue_tasks}\n")
            task_overview_file.write(f"Percentage of tasks incomplete: {percentage_incomplete:.2f}%\n")
            task_overview_file.write(f"Percentage of tasks overdue: {percentage_overdue:.2f}%\n")

        # This path creates a user overview
            
        total_users = len(username_password.keys())

        # Formats and writes the file into user_overview.txt

        with open("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(f"Total number of users: {total_users}\n")
            user_overview_file.write(f"Total number of tasks: {total_tasks}\n")

            for user in username_password.keys():
                user_tasks = [task for task in task_list if task['username'] == user]
                total_user_tasks = len(user_tasks)
                incomplete_user_tasks = total_user_tasks - completed_tasks
                overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and 
                                         task['due_date'].date() < datetime.now().date())

                # If statements to determine percentages

                if total_user_tasks > 0:
                    percentage_user_tasks = float((total_user_tasks / total_tasks) * 100)
                else:
                    percentage_user_tasks = 0

                if total_user_tasks > 0:
                    percentage_completed_user_tasks = (float(completed_tasks / total_user_tasks) * 100)
                else:
                    percentage_completed_user_tasks = 0

                if total_user_tasks > 0:
                    percentage_incomplete_user_tasks = float((incomplete_user_tasks / total_user_tasks) * 100)
                else:
                    percentage_incomplete_user_tasks = 0

                if total_user_tasks > 0:
                    percentage_overdue_user_tasks = float((overdue_user_tasks / total_user_tasks) * 100)
                else:
                    percentage_overdue_user_tasks = 0

                # Writes the calculations to the user_overview.txt file

                user_overview_file.write(f'''\nUser: {user}\n''')
                user_overview_file.write(f'''  Total number of tasks assigned: 
                                         {total_user_tasks}\n''')
                user_overview_file.write(f'''  Percentage of total tasks assigned: 
                                         {percentage_user_tasks:.2f}%\n''')
                user_overview_file.write(f'''  Percentage of completed tasks: 
                                         {percentage_completed_user_tasks:.2f}%\n''')
                user_overview_file.write(f'''  Percentage of incomplete tasks:
                                         {percentage_incomplete_user_tasks:.2f}%\n''')
                user_overview_file.write(f'''  Percentage of overdue tasks: 
                                         {percentage_overdue:.2f}%\n''')
        
    # Display statistics
    
    elif menu == display_statistics and curr_user == 'admin':
        # Checks on the system whether a report files exist, if not - this will create them.
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            # Creates a task overview.
            with open("task_overview.txt", "w") as task_overview_file:
                task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
                task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
                task_overview_file.write(f"Total number of incomplete tasks: {incomplete_tasks}\n")
                task_overview_file.write(f"Total number of tasks overdue: {overdue_tasks}\n")
                task_overview_file.write(f"Percentage of tasks incomplete: {percentage_incomplete:.2f}%\n")
                task_overview_file.write(f"Percentage of tasks overdue: %\n")
            # Creates a user overview.
            total_users = len(username_password.keys())
            with open("user_overview.txt", "w") as user_overview_file:
                user_overview_file.write(f"Total number of users: {total_users}\n")
                user_overview_file.write(f"Total number of tasks: {total_tasks}\n")

                for user in username_password.keys():
                    user_tasks = [task for task in task_list if task['username'] == user]
                    total_user_tasks = len(user_tasks)
                    incomplete_user_tasks = total_user_tasks - completed_tasks
                    overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and
                                              task['due_date'].date() < datetime.now().date())
                
                    percentage_user_tasks = float((total_user_tasks / total_tasks) * 100)
            
            # If statements to determine percentages 

            if total_user_tasks > 0:
                percentage_user_tasks = float((total_user_tasks / total_tasks) * 100)
            else:
                percentage_user_tasks = 0

            if total_user_tasks > 0:
                percentage_completed_user_tasks = (float(completed_tasks / total_user_tasks) * 100)
            else:
                percentage_completed_user_tasks = 0

            if total_user_tasks > 0:
                percentage_incomplete_user_tasks = float((incomplete_user_tasks / total_user_tasks) * 100)
            else:
                percentage_incomplete_user_tasks = 0

            if total_user_tasks > 0:
                percentage_overdue_user_tasks = float((overdue_user_tasks / total_user_tasks) * 100)
            else:
                percentage_overdue_user_tasks = 0

            #  Writes the calculations to the user_overview.txt file

            with open("user_overview.txt", "r") as user_overview_file:
                print(f"\nUser: {user}\n")
                print(f"  Total number of tasks assigned: {total_user_tasks}\n")
                print(f"  Percentage of total tasks assigned: {percentage_user_tasks:.2f}%\n")
                print(f"  Percentage of completed tasks: {percentage_completed_user_tasks:.2f}%\n")
                print(f"  Percentage of incomplete tasks: {percentage_incomplete_user_tasks:.2f}%\n")
                print(f"  Percentage of overdue tasks: {percentage_overdue_user_tasks:.2f}%\n")


            # View and display the reports
            with open("task_overview.txt", "r") as task_overview_file:
                print("\nTask Overview Report:\n" + task_overview_file.read())

            with open("user_overview.txt", "r") as user_overview_file:
                print("\nUser Overview Report:\n" + user_overview_file.read())
          
    # Exit

    elif menu == 'e':
        print('Goodbye!!!')
        # We exit the loop with False.

        logged_in = False 
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
