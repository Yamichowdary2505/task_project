import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("tasks.json")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
DATE_FORMATS = ("%Y-%m-%d", "%d-%m-%Y")


def normalize_task(task):
    if not isinstance(task, dict):
        return {"title": str(task), "done": False, "priority": "medium", "due_date": None}

    return {
        "title": str(task.get("title", "")).strip() or "Untitled Task",
        "done": bool(task.get("done", False)),
        "priority": normalize_priority(task.get("priority", "medium")),
        "due_date": normalize_due_date(task.get("due_date")),
    }


def normalize_priority(priority):
    priority_text = str(priority).strip().lower()
    if priority_text in PRIORITY_ORDER:
        return priority_text
    return "medium"


def normalize_due_date(due_date):
    if due_date in (None, ""):
        return None

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(str(due_date), date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def load_tasks():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [normalize_task(task) for task in data]


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def sort_tasks(tasks):
    return sorted(
        enumerate(tasks),
        key=lambda item: (
            item[1]["done"],
            PRIORITY_ORDER[item[1]["priority"]],
            item[1]["due_date"] or "9999-12-31",
            item[1]["title"].lower(),
        ),
    )


def show_summary(tasks):
    total = len(tasks)
    completed = sum(task["done"] for task in tasks)
    pending = total - completed
    print(f"\nSummary: {total} total | {pending} pending | {completed} completed")


def format_task(task):
    status = "Done" if task["done"] else "Pending"
    priority = task["priority"].capitalize()
    due_text = task["due_date"] if task["due_date"] else "No due date"
    return f"{task['title']} [{status}] | Priority: {priority} | Due: {due_text}"


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    sorted_tasks = sort_tasks(tasks)
    show_summary(tasks)
    print("Your Tasks:")
    for display_index, (_, task) in enumerate(sorted_tasks, start=1):
        print(f"{display_index}. {format_task(task)}")


def prompt_for_priority(default="medium"):
    raw_value = input(f"Enter priority (high/medium/low) [{default}]: ").strip().lower()
    if not raw_value:
        return default

    if raw_value in PRIORITY_ORDER:
        return raw_value

    print("Invalid priority. Using medium.")
    return "medium"


def prompt_for_due_date(default=None):
    prompt_default = default if default else "optional"
    raw_value = input(
        f"Enter due date in YYYY-MM-DD or DD-MM-YYYY [{prompt_default}]: "
    ).strip()
    if not raw_value:
        return default

    normalized = normalize_due_date(raw_value)
    if normalized is None:
        if default:
            print("Invalid date format. Keeping the previous due date.")
            return default

        print("Invalid date format. Due date skipped.")
    return normalized


def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    priority = prompt_for_priority()
    due_date = prompt_for_due_date()

    tasks.append(
        {
            "title": title,
            "done": False,
            "priority": priority,
            "due_date": due_date,
        }
    )
    save_tasks(tasks)
    print("Task added.")


def get_task_index(tasks, action_text):
    if not tasks:
        show_tasks(tasks)
        return None

    sorted_tasks = sort_tasks(tasks)
    show_tasks(tasks)

    try:
        task_number = int(input(f"Enter task number to {action_text}: ").strip())
        if 1 <= task_number <= len(sorted_tasks):
            return sorted_tasks[task_number - 1][0]
    except ValueError:
        pass

    print("Invalid task number.")
    return None


def mark_task_done(tasks):
    task_index = get_task_index(tasks, "mark as done")
    if task_index is None:
        return

    tasks[task_index]["done"] = True
    save_tasks(tasks)
    print("Task marked as done.")


def mark_task_pending(tasks):
    task_index = get_task_index(tasks, "mark as pending")
    if task_index is None:
        return

    tasks[task_index]["done"] = False
    save_tasks(tasks)
    print("Task marked as pending.")


def edit_task(tasks):
    task_index = get_task_index(tasks, "edit")
    if task_index is None:
        return

    task = tasks[task_index]
    new_title = input(f"Enter new title [{task['title']}]: ").strip()
    if new_title:
        task["title"] = new_title

    task["priority"] = prompt_for_priority(task["priority"])
    task["due_date"] = prompt_for_due_date(task["due_date"])
    save_tasks(tasks)
    print("Task updated.")


def delete_task(tasks):
    task_index = get_task_index(tasks, "delete")
    if task_index is None:
        return

    removed_task = tasks.pop(task_index)
    save_tasks(tasks)
    print(f"Deleted: {removed_task['title']}")


def main():
    tasks = load_tasks()

    while True:
        print("\nTo-Do List Menu")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Mark task as pending")
        print("5. Edit task")
        print("6. Delete task")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "":
            continue
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            mark_task_pending(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
