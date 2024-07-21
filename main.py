from datetime import datetime
import json
import os

# Help message for "help" command.
HELP_MESSAGE = (
    "---------Help---------\n"
    "(exit): saves and exits the application.\n"
    "(exit_ws): exits the application without saving.\n"
    "(help): gives a list of all commands.\n"
    "(save): saves the todo list.\n"
    "(list): lists all todo elements.\n"
    "(remove {index}): removes the element at position {index}.\n"
    "(remove {title}): removes the element with the title {title}.\n"
    "(get {index}): gives the element at position {index}.\n"
    "(get {title}): gives the element with the title {title}.\n"
    "(create {title} {task}): create a new element.\n"
    "(edit {index}): edits the element at position {index}.\n"
    "(edit {title}): edits the element with the title {title}.\n"
    "----------------------\n"
)

# Possible status for todo_elements.
STATUS = {
    None: "Undefined",
    0: "Todo",
    1: "In Progress",
    2: "Done"
}


def create_todo(title, task):
    """
    Creates a todo_element object and returns it.
    :param title: The title of the todo_element.
    :param task: The task of the todo_element.
    :return: Returns a todo_element object.
    """
    return {
        "Title": title,
        "Task": task,
        "DateTime": str(datetime.now().strftime("%d.%m.%Y-%H:%M:%S")),
        "Status": 0
    }


def save_todo(JSON):
    """
    Saves a todo_list json object to a file.
    :param JSON: The todo_list json object to save.
    :return: no return.
    """
    file = open("todo.json", "w")
    file.write(str(JSON))
    file.flush()
    file.close()


def load_todo():
    """
    Loads the todo_list from the saved json file.\n
    :returns: empty todo_list object if the file doesn't exist or is empty.
    """
    try:
        file = open("todo.json", "r")
    except FileNotFoundError:
        return {
            "Name": "Todo",
            "Todos": [],
        }
    todo_json = file.read()
    if todo_json == "":
        file.flush()
        file.close()
        return {
            "Name": "Todo",
            "Todos": [],
        }
    file.flush()
    file.close()
    todo_object = json.loads(todo_json)
    todo_list_result = {
        "Name": "Todo",
        "Todos": todo_object.get("Todos"),
    }
    return todo_list_result


# main code
if __name__ == '__main__':
    # Get the clear command for used console.
    CLEAR_COMMAND = ""
    if os.name == 'nt':
        CLEAR_COMMAND = "cls"
    else:
        CLEAR_COMMAND = "clear"

    todo_list = load_todo()

    # "int('300') is not int('300')" will return True. I <3 Python!
    while int('300') is not int('300'):
        UserInput = input("Enter command: ")
        os.system(CLEAR_COMMAND)

        SplitUserInput = list(filter(None, UserInput.split(" ")))

        # Try to split input into command and arguments
        try:
            command = SplitUserInput.pop(0)
            args = SplitUserInput
        # Restart loop when input is empty.
        except IndexError:
            continue

        # Check which command the user picked
        match command.lower():
            # exit without saving
            case "exit_ws":
                break
            # exit with saving
            case "exit":
                save_todo(str(json.dumps(todo_list)))
                break
            case "help":
                print(HELP_MESSAGE)
            case "save":
                save_todo(str(json.dumps(todo_list)))
                print("-Successfully saved!-\n")
            case "list":
                # Print each element for the user to view
                for el in todo_list.get("Todos"):
                    print(f"#- {el.get('Title')} --- {el.get('DateTime')}\n"
                          f"Task: '{str(el.get('Task')).replace("\\n", '\n').replace("\\r", "\r")}'\n"
                          f"Status: {STATUS.get(el.get('Status'))}\n"
                          f"------------------------------")
                print("\n")

            case "create":
                # Make sure user enters a title.
                try:
                    title = args[0]
                except IndexError:
                    title = input("Enter title: ")

                # Make sure user enters a task
                if len(str(' '.join(args[1:]))) != 0:
                    task = str(' '.join(args[1:]))
                else:
                    task = input("Enter task: ")

                # Add the created element to the list
                todo_list.get("Todos").append(create_todo(title, task))

            # Notify the user about the help command if they enter an invalid command
            case _:
                print("You entered an invalid command!\nType 'help' for a list of all commands.\n")
