from orm.get_session import get_session
from orm.base import Task
from shared.response import create_response, HTTPStatus
import json
from datetime import datetime, timedelta


def lambda_handler(event, context):
    session = get_session()
    try:
        task_id = event['pathParameters']['taskId']
        task = session.query(Task).filter_by(id=task_id).first()

        if not task:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "Task not found"})
        
        if task.rhythm == 0:
            session.delete(task)
        else:
            end_date = datetime.today() + timedelta(days=task.rhythm)
            task.due_date = end_date
        
        session.commit()
        return create_response(HTTPStatus.ACCEPTED, {"message": "Task set to done successfully"})

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})

    finally:
        session.close()
