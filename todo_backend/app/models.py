# PUBLIC_INTERFACE
class Task:
    """
    Represents a to-do task with an id, description, and completion status.
    """
    def __init__(self, id: int, description: str, completed: bool = False):
        self.id = id
        self.description = description
        self.completed = completed

    def to_dict(self):
        """
        Returns the task as a dictionary.
        """
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }
