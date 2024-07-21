import datetime, os, json

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
                "(create {title}): create a new element.\n"
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
        "DateTime": str(datetime.datetime.utcnow()),
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

    todo_list.get("Todos").append(create_todo("Test1", "Do something."))
    todo_list.get("Todos").append(create_todo("Test2", "Do something else."))

    while 1:
        UserInput = input("Enter command: ")
        os.system(CLEAR_COMMAND)
        match UserInput.lower():
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
                          f"Task: {el.get('Task')}\n"
                          f"Status: {STATUS.get(el.get('Status'))}\n"
                          f"------------------------------")
                print("\n")
