#!/usr/bin/env python3
"""
To‑Do List Manager Application.

This script implements a simple command‑line to‑do list manager in
Python. It allows users to create, view, update, mark as completed,
and delete tasks. Tasks are stored in a JSON file (`tasks.json`) so
that they persist between runs of the program.

Features:

* **Persistent Tasks** – Tasks are saved to `tasks.json` and loaded
  automatically at startup.

* **Add Task** – Create a new task by specifying a description and
  optional due date or notes.

* **View Tasks** – Display all tasks with their IDs, descriptions,
  statuses (Pending/Completed), and any due dates.

* **Update Task** – Modify an existing task’s description or notes.

* **Mark Task Completed/Uncompleted** – Toggle the completion status
  of a task.

* **Delete Task** – Remove a task from the list.

* **User Interface** – A menu‑driven CLI guides the user through
  available actions with clear prompts.

Usage::

    python todo_manager.py

"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


DATA_FILE = "tasks.json"


def load_tasks() -> List[Dict[str, str]]:
    """Load tasks from the JSON file or return an empty list."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [dict(task) for task in data]
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_tasks(tasks: List[Dict[str, str]]) -> None:
    """Save the list of tasks to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except IOError as exc:
        print(f"Error saving tasks: {exc}")


def generate_new_id(tasks: List[Dict[str, str]]) -> int:
    """Generate a new unique task ID based on existing tasks."""
    if not tasks:
        return 1
    existing_ids = [task.get("id", 0) for task in tasks if isinstance(task.get("id"), int)]
    return max(existing_ids, default=0) + 1


def add_task(tasks: List[Dict[str, str]]) -> None:
    """Prompt the user to create a new task."""
    print("\n=== Add New Task ===")
    description = input("Enter task description: ").strip()
    if not description:
        print("Description cannot be empty. Task not added.\n")
        return
    due_date_input = input("Enter due date (optional, YYYY-MM-DD) or leave blank: ").strip()
    due_date = ""
    if due_date_input:
        try:
            # Validate the date format; store string as provided
            datetime.strptime(due_date_input, "%Y-%m-%d")
            due_date = due_date_input
        except ValueError:
            print("Invalid date format. Due date ignored.")
    notes = input("Enter any notes (optional): ").strip()
    new_task = {
        "id": generate_new_id(tasks),
        "description": description,
        "completed": False,
        "due_date": due_date,
        "notes": notes,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!\n")


def list_tasks(tasks: List[Dict[str, str]]) -> None:
    """Display the list of tasks with their statuses."""
    print("\n=== To-Do List ===")
    if not tasks:
        print("No tasks found.\n")
        return
    for task in tasks:
        status = "Completed" if task.get("completed") else "Pending"
        due = task.get("due_date", "")
        due_str = f" (Due: {due})" if due else ""
        print(f"{task['id']}. {task['description']}{due_str} – {status}")
    print("")


def find_task_by_id(tasks: List[Dict[str, str]], task_id: int) -> Optional[Dict[str, str]]:
    """Return a task dictionary matching the given ID, or None."""
    return next((t for t in tasks if t.get("id") == task_id), None)


def update_task(tasks: List[Dict[str, str]]) -> None:
    """Update an existing task's description, due date, or notes."""
    list_tasks(tasks)
    if not tasks:
        return
    try:
        task_id = int(input("Enter the ID of the task to update (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Update cancelled.\n")
        return
    if task_id == 0:
        print("Update cancelled.\n")
        return
    task = find_task_by_id(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return
    print("Leave a field blank to keep the current value.")
    new_description = input(f"New description [{task['description']}]: ").strip()
    new_due = input(f"New due date (YYYY-MM-DD) [{task['due_date'] or 'None'}]: ").strip()
    new_notes = input(f"New notes [{task['notes'] or 'None'}]: ").strip()
    if new_description:
        task['description'] = new_description
    if new_due:
        try:
            datetime.strptime(new_due, "%Y-%m-%d")
            task['due_date'] = new_due
        except ValueError:
            print("Invalid date format. Due date not updated.")
    if new_notes:
        task['notes'] = new_notes
    save_tasks(tasks)
    print("Task updated successfully!\n")


def toggle_completion(tasks: List[Dict[str, str]]) -> None:
    """Mark a task as completed or uncompleted."""
    list_tasks(tasks)
    if not tasks:
        return
    try:
        task_id = int(input("Enter the ID of the task to toggle completion (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Operation cancelled.\n")
        return
    if task_id == 0:
        print("Operation cancelled.\n")
        return
    task = find_task_by_id(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return
    task['completed'] = not task.get('completed', False)
    status = "completed" if task['completed'] else "pending"
    save_tasks(tasks)
    print(f"Task marked as {status}.\n")


def delete_task(tasks: List[Dict[str, str]]) -> None:
    """Remove a task from the list."""
    list_tasks(tasks)
    if not tasks:
        return
    try:
        task_id = int(input("Enter the ID of the task to delete (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Deletion cancelled.\n")
        return
    if task_id == 0:
        print("Deletion cancelled.\n")
        return
    task = find_task_by_id(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return
    confirm = input(f"Are you sure you want to delete '{task['description']}'? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        tasks.remove(task)
        save_tasks(tasks)
        print("Task deleted successfully!\n")
    else:
        print("Deletion aborted.\n")


def main_menu() -> None:
    """Main loop for the to‑do list manager."""
    tasks = load_tasks()
    actions = {
        "1": add_task,
        "2": list_tasks,
        "3": update_task,
        "4": toggle_completion,
        "5": delete_task,
        "6": lambda _: exit(0),
    }
    while True:
        print("=== To-Do List Manager ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Task Completed/Uncompleted")
        print("5. Delete Task")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()
        action = actions.get(choice)
        if action:
            action(tasks)
        else:
            print("Invalid selection. Please choose a valid option.\n")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")