from typing import List, Optional
from .models import Task


# PUBLIC_INTERFACE
class TaskService:
    """
    Service class to manage Task objects in memory.
    Provides add, retrieve, update, and delete operations.
    """

    def __init__(self):
        self._tasks = {}  # id -> Task
        self._next_id = 1

    # PUBLIC_INTERFACE
    def add_task(self, description: str) -> Task:
        """Add a new task with the next available id and return it."""
        task = Task(id=self._next_id, description=description, completed=False)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    # PUBLIC_INTERFACE
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its id. Returns None if not found."""
        return self._tasks.get(task_id)

    # PUBLIC_INTERFACE
    def list_tasks(self) -> List[Task]:
        """Return a list of all tasks."""
        return list(self._tasks.values())

    # PUBLIC_INTERFACE
    def update_task(
        self,
        task_id: int,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """
        Update a task's description or completed status.
        Returns the updated task or None if not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            return None
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        return task

    # PUBLIC_INTERFACE
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its id. Returns True if deleted, False if not found.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
