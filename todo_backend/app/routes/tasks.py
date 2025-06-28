from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from app.task_service import TaskService

blp = Blueprint(
    "Tasks", "tasks", url_prefix="/tasks",
    description="Endpoints to manage to-do tasks."
)

# In-memory singleton service instance
task_service = TaskService()


class TaskSchema(Schema):
    id = fields.Int(dump_only=True, description="Task ID")
    description = fields.Str(required=True, description="Task description")
    completed = fields.Bool(required=True, description="Completion status")


class TaskCreateSchema(Schema):
    description = fields.Str(required=True, description="Description of the new task")


class TaskUpdateSchema(Schema):
    completed = fields.Bool(required=True, description="Mark completed")


@blp.route("/")
class TasksCollection(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """
        Get all tasks.

        Returns a list of all tasks in the to-do list.
        """
        tasks = [t.to_dict() for t in task_service.list_tasks()]
        return tasks, 200

    # PUBLIC_INTERFACE
    @blp.arguments(TaskCreateSchema)
    @blp.response(201, TaskSchema)
    def post(self, new_data):
        """
        Add a new task.

        Args:
            new_data (dict): New task data (description).

        Returns:
            dict: The created task.
        """
        new_task = task_service.add_task(new_data["description"])
        return new_task.to_dict(), 201


@blp.route("/<int:task_id>")
class TaskResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def patch(self, patch_data, task_id):
        """
        Complete a task (or update completed status).

        Args:
            patch_data (dict): Contains 'completed' boolean.
            task_id (int): ID of the task to update.
        Returns:
            dict: The updated task, or 404 if not found.
        """
        updated = task_service.update_task(task_id=task_id, completed=patch_data.get("completed"))
        if updated:
            return updated.to_dict(), 200
        return {"message": "Task not found"}, 404

    # PUBLIC_INTERFACE
    def delete(self, task_id):
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete.

        Returns:
            dict: Success status or 404 if not found.
        """
        deleted = task_service.delete_task(task_id)
        if deleted:
            return {"message": "Task deleted"}, 200
        return {"message": "Task not found"}, 404
