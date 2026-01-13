from datetime import datetime
from threading import Lock, Thread
from enum import Enum
import pprint
import concurrent.futures 
import time
import random


class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    def __init__(self, task_id, title, description, due_date, priority):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = Status.PENDING
        self.assigned_to = None
        self.created_at = datetime.now()
        self.completed_at = None

    def mark_completed(self):
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.tasks = {}

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]


class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.lock = Lock()
        self._task_counter = 0

    def create_user(self, user_id, name):
        self.users[user_id] = User(user_id, name)

    def create_task(self, title, description, due_date, priority, owner_id):
        print(f"Task {self._task_counter}:{title} started ")
        self.lock.acquire()
        try:
            self._task_counter += 1
            task = Task(
                task_id=self._task_counter,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority
            )
            self.tasks[self._task_counter] = task
            self.users[owner_id].add_task(task)
            self.lock.release()
        
        except KeyError:
            self.lock.release()
            print(f"User {owner_id} Not Found")
        
        except Exception as e:
            self.lock.release()
            raise Exception(f"Error: {e}")
        else:
            time.sleep(random.randint(0,3))
            print(f"Task {self._task_counter}:{title} created ")
            return task
        return 


            # time.sleep(random.randint(0,5))
            
            

    def assign_task(self, task_id, user_id):
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                task.assigned_to = user_id
                self.users[user_id].add_task(task)
                # time.sleep(random.randint(0,5))
                print(f"task {task.title} assigned to user {user_id}")

    def update_task(self, task_id, **updates):
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                task.update(**updates)

    def delete_task(self, task_id):
        with self.lock:
            task = self.tasks.pop(task_id, None)
            if task:
                for user in self.users.values():
                    user.tasks.pop(task_id, None)

    def search_tasks(self, **filters):
        results = self.tasks.values()
        for attr, value in filters.items():
            results = filter(lambda t: getattr(t, attr) == value, results)
        return list(results)

    def get_task_history(self, user_id):
        return [
            task for task in self.users[user_id].tasks.values()
            if task.status == Status.COMPLETED
        ]

if __name__ == "__main__":
    manager = TaskManager()

    manager.create_user(1, "Tanishk")
    manager.create_user(2, "Vashit")

    tasks = {
        "task1" : {
            "title" : "Assignment-1",
            "description" : "Complete the assignment on week1 and week2",
            "due_date" :datetime(2026, 1, 13),
            "priority" : Priority.HIGH,
            "owner_id" : 1
        },
        "task2" : {
            "title" : "Assignment-2",
            "description" : "Complete the assignment on week3",
            "due_date" :datetime(2026, 1, 20),
            "priority" : Priority.HIGH,
            "owner_id" : 1
        },
        "task3" : {
            "title" : "Assignment-3",
            "description" : "Complete the assignment on week4",
            "due_date" :datetime(2026, 1, 27),
            "priority" : Priority.HIGH,
            "owner_id" : 1
        }

    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        created_taskes = [executor.submit(manager.create_task, task["title"], task["description"], task["due_date"], task["priority"], task["owner_id"]) for _, task in tasks.items()]
        # for f in concurrent.futures.as_completed(created_taskes):
        #     print(f.result())

    with concurrent.futures.ThreadPoolExecutor() as executor:
        assigned_task = [executor.submit(manager.assign_task, task.result().task_id, 2) for task in concurrent.futures.as_completed(created_taskes)]
    
    concurrent.futures.wait(assigned_task)
    print("Program completed")

    


    # manager.update_task(task.task_id, status=Status.IN_PROGRESS)
    # task.mark_completed()

    # history = manager.get_task_history(2)
    # print([t.title for t in history])
