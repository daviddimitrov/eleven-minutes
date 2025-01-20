from orm.get_session import get_session
from orm.base import Task
from shared.response import create_response, HTTPStatus
import json


def lambda_handler(event, context):
    session = get_session()
    try:
        # Parse the request body
        body = json.loads(event['body'])

        # Create a new Task object
        new_task = Task(
            priority_level_id=body.get("priority_level_id"),
            user_id=body.get("user_id"),
            name=body.get("name"),
            duration=body.get("duration"),
            due_date=body.get("dueDate"),
            rhythm=body.get("rhythm"),
            today=body.get("today"),
        )

        # Add and commit the new task to the database
        session.add(new_task)
        session.commit()

        # Close the session
        session.close()

        # Return success response
        return create_response(HTTPStatus.CREATED, {
            "message": "Task created successfully",
            "task": {
                "id": new_task.id,  # Assuming Task has an auto-generated ID
                "userId": new_task.user_id,
                "priorityLevel": new_task.priority_level_id,
                "name": new_task.name,
                "duration": new_task.duration,
                "dueDate": new_task.due_date,
                "rhythm": new_task.rhythm,
                "today": new_task.today,
            },
        })

    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {
            "message": "An error occurred",
            "error": str(e),
        })
    finally:
        session.close()
