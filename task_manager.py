# Import datetime module to handle date and time operations.
from datetime import datetime

USER_PATH = "user.txt"
TASK_PATH = "tasks.txt"


def login():
    """
    This function will handle user login.
    - It will read usernames and passwords from the user.txt file.
    - It will use a while loop to validate the username and password.
    - If the login is successful, it will return the username.
    - If the login fails, it will prompt the user to try again.
    """
    print("Welcome to the Task Management System!\n")

    try:
        with open(USER_PATH, "r", encoding="utf-8") as file:
            users = {}
            for line in file:
                username, password = line.strip().split(", ")
                users[username] = password
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username in users and users[username] == password:
                print(f"Welcome {username}!\n")
                return username
            else:
                print("Invalid username or password. Please try again.")
    except FileNotFoundError:
        print("User file not found. Please ensure user.txt exists.")
        exit()


authenticated_user = login()


def reg_user():
    """
    This code block will add a new user to the user.txt file
    - Request input of a new username
    - Request input of a new password
    - Request input of password confirmation.
    - Check if the new password and confirmed password are the same
    - If they are the same, add them to the user.txt file,
    otherwise present a relevant message
    """
    print("Register a new user\n")
    try:
        with open(USER_PATH, "a+", encoding="utf-8") as file:
            while True:
                username = input("Enter a new username: ")
                # Move to the beginning of the file to read existing usernames
                file.seek(0)
                # Check if the username already exists
                if username in file.read():
                    print(
                        "Username already exists. "
                        "Please choose a different username."
                    )
                    continue
                password = input("Enter a new password: ")
                password_confirm = input("Confirm your password: ")
                if password == password_confirm:
                    with open(USER_PATH, "a+", encoding="utf-8") as file:
                        file.seek(0)
                        content = file.read()
                        # If the file is not empty, doesn"t end with a newline, add one
                        if content and not content.endswith("\n"):
                            file.write("\n")

                        # Then write the new user on a new line
                        file.write(f"{username}, {password}\n")
                    print(f"User {username} registered successfully!\n")
                    break
    except FileNotFoundError:
        print("Cannot register user.")


def view_all():
    """This code block will read the task from task.txt file and
    print to the console in the format of Output 2 presented in the PDF
    You can do it in this way:
       - Read a line from the file.
       - Split that line where there is comma and space.
       - Then print the results in the format shown in the Output 2 in
         the PDF
       - It is much easier to read a file using a for loop."""
    print("Viewing all tasks\n")

    try:
        with open(TASK_PATH, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                (assigned_to,
                 task,
                 description,
                 date_assigned,
                 due_date,
                 completed) = (
                    line.strip().split(", ")
                )
                print(
                    f"""
    ____________________________________________________________

    Task {i+1} :              {task}.
    Assigned to:          {assigned_to}.
    Date assigned:        {date_assigned}.
    Due Date:             {due_date}.
    Description:          {description}.
    Task Complete?:       {completed}.
    ____________________________________________________________
                      """
                )
    except FileNotFoundError:
        print("Task file not found. Please ensure task.txt exists.")


def date_format(date):
    """
    This will convert the date from DD-MM-YYYY to a more readable format.
    - It will take a date string as input.
    - It will return the date in the format "DD-MMM-YYYY".
    """
    date_formats = ["%d-%m-%Y", "%d/%m/%Y", "%d%m%Y", "%d %m %Y"]

    for fmt in date_formats:
        try:
            # Try to parse input using the current format
            parsed_date = datetime.strptime(date, fmt)
            formatted_date = parsed_date.strftime("%d %b %Y")
            return formatted_date
        except ValueError:
            continue
    print("Invalid date format for", fmt)


def get_valid_task_number(user_tasks):
    """
    This function will repeatedly prompt the user for a task number until a
    valid one is provided or return to main menu when -1 is entered.
    """

    try:
        task_number = int(
            input("Enter a task number to edit/mark complete or -1 for main menu: ")
        )
        if task_number == -1:
            return

        if 1 <= task_number <= len(user_tasks):
            task_index, selected_task_line = user_tasks[task_number - 1]
            return task_index, selected_task_line.strip()
        else:
            print(f"\nTask {task_number} does not exist. Try again.\n")
            return get_valid_task_number(user_tasks)
    except ValueError:
        print("\nPlease enter a valid number.\n")
        return get_valid_task_number(user_tasks)


def view_mine(current_user):
    """This code block will read the task from task.txt file and will:
    - Read a line from the file.
    - Split that line where there is comma and space.
    - Check if the username of the person logged in is the same as the
      username you have read from the file.
    - If they are the same you print the task in a user friendly format as
    """
    print(f"Viewing tasks for {current_user}\n")

    try:
        with open(TASK_PATH, "r", encoding="utf-8") as file:
            tasks = file.readlines()

        user_tasks = []
        for index, line in enumerate(tasks):
            (assigned_to,
             title,
             description,
             date_assigned,
             due_date,
             completed) = (
                line.strip().split(", ")
            )
            if assigned_to.lower() == current_user.lower():
                user_tasks.append((index, line))
                print(
                    f"""
    ____________________________________________________________

    Task :                {len(user_tasks)}.
    Assigned to:          {assigned_to}.
    Date assigned:        {date_assigned}.
    Due Date:             {due_date}.
    Description:          {description}.
    Task Complete?:       {completed}.
    ____________________________________________________________
                          """
                )

        if not user_tasks:
            print("You have no tasks assigned.\n")
            return

        task_info = get_valid_task_number(user_tasks)
        if not task_info:
            return

        task_index, task_line = task_info

        assigned_to, title, description, date_assigned, due_date, completed = (
            task_line.split(", ")
        )

        # Ask what to do with the selected task
        while True:
            print(
                """
        1 - Mark as complete
        2 - Edit task
        3 - Exit to main menu
        """
            )
            option = input("Choose an option: ")

            (assigned_to,
             title,
             description,
             date_assigned,
             due_date,
             completed) = (
                task_line.strip().split(", ")
            )

            if option == "1":
                # Mark as complete
                if completed.lower() == "yes":
                    print("This task is already marked as complete.")
                else:
                    tasks[task_index] = (
                        f"""{assigned_to},
                        {title},
                        {description},
                        {date_assigned},
                        {due_date},
                        Yes\n
                        """
                    )
                    with open(TASK_PATH, "w", encoding="utf-8") as file:
                        file.writelines(tasks)
                    print("Task marked as complete.\n")
                    return

            elif option == "2":
                if completed.lower() == "yes":
                    print("You cannot edit a completed task.")
                    return

                # Edit assigned user
                new_user = input(
                  f'Enter new username (or press Enter to keep "{assigned_to}"): '
                )
                if new_user.strip() == "":
                    new_user = assigned_to

                # Edit due date
                new_due_date = input(
                    f'Enter new due date (DD-MM-YYYY) or press Enter to keep "{due_date}": '
                )
                if new_due_date.strip() == "":
                    new_due_date = due_date
                else:
                    try:
                        # Validate date format
                        new_due_date = date_format(new_due_date)
                    except ValueError:
                        print("Invalid date format. Keeping original due date.")
                        new_due_date = due_date

                # Update the task selected
                tasks[task_index] = (
                    f"""{new_user},
                    {title},
                    {description},
                    {date_assigned},
                    {new_due_date},
                    {completed}
                    \n"""
                )
                with open(TASK_PATH, "w", encoding="utf-8") as file:
                    file.writelines(tasks)
                print("\nTask updated successfully.\n")
            elif option == "3":
                print("\nExiting to main menu.\n")
                return
            else:
                print("\nInvalid option selected, please try again.\n")

    except FileNotFoundError:
        print("tasks.txt file not found.")


def view_completed():
    """
    This code block will view all task that have been completed.
    It will read the tasks from task.txt file and print only tasks that have
    been marked completed.
    """
    print("Viewing completed tasks\n")
    try:
        with open(TASK_PATH, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                (assigned_to,
                 task,
                 description,
                 date_assigned,
                 due_date,
                 completed) = (
                    line.strip().split(", ")
                )
                if completed.lower() == "yes":
                    print(
                        f"""
    ____________________________________________________________

    Task {i+1}:               {task}.
    Assigned to:          {assigned_to}.
    Date assigned:        {date_assigned}.
    Due Date:             {due_date}.
    Description:          {description}.
    Task Complete?:       {completed}.
    ____________________________________________________________
                          """
                    )
    except FileNotFoundError:
        print("Task file not found.")


def delete_task():
    """Marks a task as completed by updating the "No" to "Yes" in the task
    file."""
    print("Marking a task as completed\n")

    while True:
        try:
            with open(TASK_PATH, "r", encoding="utf-8") as file:
                tasks = file.readlines()
            for i, line in enumerate(tasks):
                (assigned_to,
                 task,
                 description,
                 date_assigned,
                 due_date,
                 completed) = (
                    line.strip().split(", ")
                )
                print(
                    f"""
    ____________________________________________________________

    Task {i+1} :              {task}.
    Assigned to:          {assigned_to}.
    Date assigned:        {date_assigned}.
    Due Date:             {due_date}.
    Description:          {description}.
    Task Complete?:       {completed}.
    ____________________________________________________________
                      """
                )
            task_number = int(
                input(
                    "Enter the number of the task to mark as completed or -1 to return to the main menu: "
                )
            )
            if task_number == -1:
                return

            if task_number < 1 or task_number > len(tasks):
                print(f"Task {task_number} does not exist. Please try again.\n")
                continue

            del tasks[task_number - 1]

            with open(TASK_PATH, "w", encoding="utf-8") as file:
                file.writelines(tasks)

            print(f"Task {task_number} delete completed successfully.\n")
            return

        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
        except FileNotFoundError:
            print("Task file not found.")
            return


def add_task():
    """This code block will allow a user to add a new task to task.txt file
    - You can use these steps:
        - Prompt a user for the following:
            - the username of the person whom the task is assigned to,
            - the title of the task,
            - the description of the task, and
            - the due date of the task.
        - Then, get the current date.
        - Add the data to the file task.txt
        - Remember to include "No" to indicate that the task is not
          complete.
    """
    print("Adding a new task\n")
    assigned_to = input("Enter the username of the person the task is assigned to: ")
    task = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    due_date = date_format(input("Enter the due date of the task (DD-MM-YYYY): "))
    date_assigned = datetime.now().strftime("%d %b %Y")
    completed = "No"

    try:
        new_task = f"{assigned_to}, {task}, {description}, {date_assigned}, {due_date}, {completed}"
        # Check if the file exists and if it starts with an empty line
        with open(TASK_PATH, "a+", encoding="utf-8") as file:
            file.seek(0)
            task_content = file.read()

            # If the file is not empty and doesn"t end with a newline, add one
            if task_content and not task_content.endswith("\n"):
                file.write("\n")

            # Then write the new task on a new line
            file.write(f"{new_task}\n")
        print("\nTask added successfully.")

    except FileNotFoundError:
        print("\nFile not found.")


def display_statistics():
    """
    This function will display statistics about tasks and users.
    - It will read the tasks from the tasks.txt and user.txt file.
    - Then display the total number of tasks, completed tasks, pending tasks,
      and overdue tasks.
    - It will also display the total number of users and their task statistics.
    """
    try:
        generate_report()
    except FileNotFoundError:
        print("Report files not found.")

    print("\nTASK OVERVIEW")
    print("_______________________________________________________")
    try:
        with open("task_overview.txt", "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("task_overview.txt not found.")

    print("\nUSER OVERVIEW")
    print("_____________________________________________________")
    try:
        with open("user_overview.txt", "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("user_overview.txt not found.")
    return


def generate_report():
    """
    This function will generate a report of all tasks and users.
    - It will read the tasks from the tasks.txt file.
    - It will count the number of tasks, completed tasks, and pending tasks.
    - It will save the report to task_overview.txt for tasks and user_overview.txt for users.
    """
    print("Generating report...\n")

    def task_overview():
        try:
            with open(TASK_PATH, "r", encoding="utf-8") as file:
                tasks = file.readlines()
            if len(tasks) == 0:
                print("No tasks found.")
            else:
                total_tasks = len(tasks)
                completed_tasks = sum(
                    1 for task in tasks if task.strip().endswith("Yes")
                )
                pending_tasks = total_tasks - completed_tasks
                # Compare date now with due date to find overdue dte
                overdue_tasks = sum(
                    1
                    for task in tasks
                    if task.strip().split(", ")[4] != "None"
                    and datetime.strptime(task.strip().split(", ")[4], "%d %b %Y")
                    < datetime.now()
                )

                if total_tasks > 0:
                    incomplete_tasks = (pending_tasks / total_tasks) * 100
                    overdue_tasks_percentage = (overdue_tasks / total_tasks) * 100
                else:
                    print("No tasks to calculate statistics.")
                    return

                with open(
                    "C:\\Users\\ttsatsi\\Documents\\Hyperion Dev\\M03\\Capstone\\task_overview.txt",
                    "w+",
                    encoding="utf-8",
                ) as file:
                    file.write(f"Total Tasks: {total_tasks}\n")
                    file.write(f"Completed Tasks: {completed_tasks}\n")
                    file.write(f"Pending Tasks: {pending_tasks}\n")
                    file.write(f"Overdue Tasks: {overdue_tasks}\n")
                    file.write(f"Incomplete Tasks: {incomplete_tasks:.2f}%\n")
                    file.write(
                        f"Overdue Tasks Percentage: {overdue_tasks_percentage:.2f}%\n"
                    )

        except FileNotFoundError:
            print("Task file not found.")

    def user_overview():
        try:
            with open(USER_PATH, "r", encoding="utf-8") as user_file:
                users = [line.strip().split(", ")[0] for line in user_file]

            with open(TASK_PATH, "r", encoding="utf-8") as task_file:
                tasks = task_file.readlines()

            if len(tasks) == 0:
                print("No tasks found.")
                return

            total_tasks = len(tasks)
            total_users = len(users)

            with open(
                "C:\\Users\\ttsatsi\\Documents\\Hyperion Dev\\M03\\Capstone\\user_overview.txt",
                "w+",
                encoding="utf-8",
            ) as file:
                file.write(f"Total Users: {total_users}\n")
                file.write(f"Total Tasks: {total_tasks}\n\n")

                for user in users:
                    user_tasks = [
                        task for task in tasks if task.startswith(user + ", ")
                    ]
                    user_total = len(user_tasks)
                    user_completed = sum(
                        1 for task in user_tasks if task.strip().endswith("Yes")
                    )
                    user_incomplete = user_total - user_completed
                    user_overdue = sum(
                        1
                        for task in user_tasks
                        if task.strip().endswith("No")
                        and datetime.strptime(task.strip().split(", ")[4], "%d %b %Y")
                        < datetime.now()
                    )

                    if user_total > 0:
                        total_task_percentage = (
                            user_total / total_tasks) * 100
                        completed_percentage = (
                            user_completed / user_total) * 100
                        incomplete_percentage = (
                            user_incomplete / user_total) * 100
                        overdue_percentage = (user_overdue / user_total) * 100
                    else:
                        # Default to 0% if there no tasks
                        total_task_percentage = completed_percentage = (
                            incomplete_percentage
                        ) = overdue_percentage = 0.0

                    file.write(f"User: {user}\n")
                    file.write(f"Total Assigned Tasks: {user_total}\n")
                    file.write(
                        f"Percentage of Total Tasks: {total_task_percentage:.2f}%\n"
                    )
                    file.write(
                        f"Percentage Completed Tasks: {completed_percentage:.2f}%\n"
                    )
                    file.write(
                        f"Percentage Incomplete Tasks: {incomplete_percentage:.2f}%\n"
                    )
                    file.write(
                        f"Percentage Overdue and Incomplete Tasks: {overdue_percentage:.2f}%\n\n"
                    )

        except FileNotFoundError:
            print("User file not found.")
        print(
            "Report generated successfully. Check task_overview.txt"
            " and user_overview.txt for details."
        )

    task_overview()
    user_overview()


while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case for comparison.
    if authenticated_user == "admin":
        print(f"Welcome {authenticated_user}! You can manage users and tasks.")

        menu = input(
            """Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    vc - view completed tasks
    del - delete a task
    ds - display statistics
    gr - generate reports
    e - exit
    : """
        ).lower()

        if menu == "r":
            reg_user()

        elif menu == "a":
            add_task()

        elif menu == "va":
            view_all()

        elif menu == "vm":
            view_mine(authenticated_user)

        elif menu == "vc":
            view_completed()

        elif menu == "del":
            delete_task()

        elif menu == "ds":
            display_statistics()

        elif menu == "gr":
            generate_report()

        elif menu == "e":
            print("Goodbye!!!")
            exit()  # Break is an option

        else:
            print("You have entered an invalid input. Please try again")
    else:
        print(f"Welcome {authenticated_user}! You can manage your tasks.")
        menu = input(
            """Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : """
        ).lower()

        if menu == "a":
            add_task()

        elif menu == "va":
            view_all()

        elif menu == "vm":
            view_mine(authenticated_user)

        elif menu == "e":
            print("Goodbye!!!")
            exit()

        else:
            print("You have entered an invalid input. Please try again")
