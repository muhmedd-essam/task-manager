import json
from datetime import datetime


class Task:
    def __init__(self, title, description, due_date, status="incomplete"):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.status = status

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {self.status}"


class PersonalTask(Task):
    def __init__(self, title, description, due_date, category, status):
        super().__init__(title, description, due_date, status)
        self.category = category

    def get_task_type(self):
        return "Personal"


class WorkTask(Task):
    def __init__(self, title, description, due_date, priority, status):
        super().__init__(title, description, due_date, status)
        self.priority = priority

    def get_task_type(self):
        return "Work"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task):
        self.tasks.remove(task)

    def update_due_date(self, task, new_due_date):
        task.due_date = datetime.strptime(new_due_date, "%Y-%m-%d")

    def mark_task_completed(self, task):
        task.status = "completed"

    def show_tasks(self):
        for task in self.tasks:
            print(task)
            print()

    def save_tasks_to_json(self, filename):
        data = []
        for task in self.tasks:
            task_data = {
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date.strftime("%Y-%m-%d"),
                "status": task.status,
                "type": task.get_task_type(),
            }
            if isinstance(task, PersonalTask):
                task_data["category"] = task.category
            elif isinstance(task, WorkTask):
                task_data["priority"] = task.priority
            data.append(task_data)

        with open(filename, "w") as file:
            json.dump(data, file)

    def load_tasks_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        for task_data in data:
            title = task_data["title"]
            description = task_data["description"]
            due_date = task_data["due_date"]
            status = task_data["status"]
            task_type = task_data["type"]

            if task_type == "Personal":
                category = task_data["category"]
                task = PersonalTask(title, description, due_date, category, status)
            elif task_type == "Work":
                priority = task_data["priority"]
                task = WorkTask(title, description, due_date, priority, status)
            else:
                task = Task(title, description, due_date, status)

            self.add_task(task)


def main():
    task_manager = TaskManager()

    while True:
        print("1. Add a task")
        print("2. Delete a task")
        print("3. Show list of tasks")
        print("4. Update due date")
        print("5. Mark task as completed")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        try:
            if choice == "1":
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                due_date = input("Enter task due date (YYYY-MM-DD): ")
                task_type = input("Enter task type (personal/work): ")

                if task_type == "personal":
                    category = input("Enter task category: ")
                    task = PersonalTask(title, description, due_date, category, "incomplete")
                elif task_type == "work":
                    priority = int(input("Enter task priority (1-5): "))
                    task = WorkTask(title, description, due_date, priority, "incomplete")
                else:
                    task = Task(title, description, due_date)

                task_manager.add_task(task)
                print("Task added successfully!")

            elif choice == "2":
                if not task_manager.tasks:
                    print("No tasks to delete.")
                    continue

                print("Select a task to delete:")
                for i, task in enumerate(task_manager.tasks):
                    print(f"{i + 1}. {task.title}")

                task_index = int(input("Enter the task number: ")) - 1

                try:
                    task = task_manager.tasks[task_index]
                    task_manager.delete_task(task)
                    print("Task deleted successfully!")
                except IndexError:
                    print("Invalid task number!")

            elif choice == "3":
                if not task_manager.tasks:
                    print("No tasks available.")
                else:
                    task_manager.show_tasks()

            elif choice == "4":
                if not task_manager.tasks:
                    print("No tasks available.")
                    continue

                print("Select a task to update the due date:")
                for i, task in enumerate(task_manager.tasks):
                    print(f"{i + 1}. {task.title}")

                task_index = int(input("Enter the task number: ")) - 1

                try:
                    task = task_manager.tasks[task_index]
                    new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                    task_manager.update_due_date(task, new_due_date)
                    print("Due date updated successfully!")
                except IndexError:
                    print("Invalid task number!")

            elif choice == "5":
                if not task_manager.tasks:
                    print("No tasks available.")
                    continue

                print("Select a task to mark as completed:")
                for i, task in enumerate(task_manager.tasks):
                    print(f"{i + 1}. {task.title}")

                task_index = int(input("Enter the task number: ")) - 1

                try:
                    task = task_manager.tasks[task_index]
                    task_manager.mark_task_completed(task)
                    print("Task marked as completed!")
                except IndexError:
                    print("Invalid task number!")

            elif choice == "6":
                filename = input("Enter the filename to save tasks (e.g., tasks.json): ")
                task_manager.save_tasks_to_json(filename)
                print("Tasks saved to file. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please try again.")

        print()


if __name__ == "__main__":
    main()