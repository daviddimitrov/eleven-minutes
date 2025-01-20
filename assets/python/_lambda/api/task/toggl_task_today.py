from orm.get_session import get_session
from orm.base import Task
from shared.response import create_response, HTTPStatus


def lambda_handler(event, context):
    session = get_session()
    try:
        task_id = event['pathParameters']['taskId']
        task = session.query(Task).filter_by(id=task_id).first()

        if not task:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "Task not found"})
        
        if task.today == 0:
            task.today = 1
        else:
            task.today = 0
        
        session.commit()
        return create_response(HTTPStatus.ACCEPTED, {"message": f"Task today set to {task.today} successfully"})

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})

    finally:
        session.close()
