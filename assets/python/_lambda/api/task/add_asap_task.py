from orm.get_session import get_session
from orm.base import AsapTask
from shared.response import create_response, HTTPStatus
import json


def lambda_handler(event, context):
    session = get_session()
    try:
        query_params = event.get('queryStringParameters', {})
        task_name = query_params.get('name')
        user_id = event['pathParameters']['userId']

        if not task_name:
            return create_response(HTTPStatus.BAD_REQUEST, {"message": "Task name is required."})
        if not user_id:
            return create_response(HTTPStatus.BAD_REQUEST, {"message": "User ID is required."})

        asap_task = AsapTask(
            user_id=user_id,
            name=task_name,
            deleted=False
        )
        session.add(asap_task)
        session.commit()
        session.close()
        return create_response(HTTPStatus.ACCEPTED, {"message": "ASAP task added successfully"})
    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()