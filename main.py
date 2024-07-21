import datetime
import json
import os

HELP_MESSAGE = ("---------Help---------\n"
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
                "----------------------\n")

STATUS = {
    None: "Undefined",
    0: "Todo",
    1: "In Progress",
    2: "Done",
}

def create_todo(title, task):
    Todo = {
        "Title": title,
        "Task": task,
        "DateTime": str(datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")),
        "Status": 0,
    }
    return Todo


def save_todo(JSON):
    file = open("todo.json", "w")
    file.write(str(JSON))
    file.flush()
    file.close()


def load_todo():
    try:
        file = open("todo.json", "r")
    except:
        return ""
    todo_json = file.read()
    if todo_json == "":
        return ""
    file.flush()
    file.close()
    todo_object = json.loads(todo_json)
    todo_list_result = {
        "Name": "TestList",
        "Todos": todo_object.get("Todos"),
    }
    return todo_list_result


if __name__ == '__main__':
    CLEAR_COMMAND = ""
    if os.name == 'nt':
        CLEAR_COMMAND = "cls"
    else:
        CLEAR_COMMAND = "clear"

    todo_list = {
        "Name": "TestList",
        "Todos": [],
    }

    if load_todo() != "":
        todo_list = load_todo()

    while 1:
        UserInput = input("Enter command: ")
        os.system(CLEAR_COMMAND)
        SplitUserInput = list(filter(None, UserInput.split(" ")))
        try:
            command = SplitUserInput.pop(0)
            args = SplitUserInput
        except IndexError:
            command = ""
            args = []
        match command.lower():
            case "exit_ws":
                break
            case "exit":
                save_todo(str(json.dumps(todo_list)))
                break
            case "help":
                print(HELP_MESSAGE)
            case "save":
                save_todo(str(json.dumps(todo_list)))
                print("-Successfully saved!-\n")
            case "list":
                for el in todo_list.get("Todos"):
                    print(f"#- {el.get('Title')} --- {el.get('DateTime')}\n"
                          f"Task: '{str(el.get('Task')).replace("\\n", '\n').replace("\\r", "\r")}'\n"
                          f"Status: {STATUS.get(el.get('Status'))}\n"
                          f"------------------------------")
                print("\n")
            case "create":
                try:
                    title = args[0]
                except IndexError:
                    title = input("Enter title: ")
                if len(str(' '.join(args[1:]))) != 0:
                    task = str(' '.join(args[1:]))
                else:
                    task = input("Enter task: ")

                todo_list.get("Todos").append(create_todo(title, task))
