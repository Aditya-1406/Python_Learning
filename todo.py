


def create_list():
    """Create a new to-do list."""
    return []

def add_task(todo_list, task):
    """Add a task to the to-do list."""
    todo_list.append(task)

def remove_task(todo_list, task):
    """Remove a task from the to-do list."""
    if task in todo_list:
        todo_list.remove(task)
    else:
        print("Task not found in the list.")

def view_tasks(todo_list):
    """View all tasks in the to-do list."""
    if not todo_list:
        print("No tasks in the to-do list.")
    else:
        for idx, task in enumerate(todo_list, start=1):
            print(f"{idx}. {task}")

def update_task(todo_list, old_task, new_task):
    """Update a task in the to-do list."""
    if old_task in todo_list:
        index = todo_list.index(old_task)
        todo_list[index] = new_task
    else:
        print("Task not found in the list.")

def main():
    todo_list = create_list()
    while True:
        print("\nTo-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Update Task")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            view_tasks(todo_list)
        elif choice == '2':
            task = input("Enter the task to add: ")
            add_task(todo_list, task)
            print("Task added.")
        elif choice == '3':
            task = input("Enter the task to remove: ")
            remove_task(todo_list, task)
        elif choice == '4':
            old_task = input("Enter the task to update: ")
            new_task = input("Enter the new task: ")
            update_task(todo_list, old_task, new_task)
        elif choice == '5':
            print("Exiting the To-Do List application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()