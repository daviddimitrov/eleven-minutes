from orm.get_session import get_session
from orm.base import Task
from shared.response import create_response, HTTPStatus
import json


def lambda_handler(event, context):
    session = get_session()
    try:
        task_id = event['pathParameters']['taskId']
        body = json.loads(event['body'])

        task = session.query(Task).filter_by(id=task_id).first()

        if not task:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "Task not found"})
        
        task.priority_level_id = body["priorityLevel"]["id"]
        task.name = body.get("name")
        task.duration = body.get("duration")
        task.due_date = body.get("dueDate")
        task.rhythm = body.get("rhythm")

        # Commit the changes to the database
        session.commit()

        # Close the session
        session.close()

        # Return success response
        return create_response(HTTPStatus.ACCEPTED, {"message": "Task updated successfully"})
    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()