from orm.get_session import get_session
from orm.base import AsapTask
from shared.response import create_response, HTTPStatus
import json


def lambda_handler(event, context):
    session = get_session()
    try:
        asap_task_id = event['pathParameters']['asapTaskId']

        asap_task = session.query(AsapTask).filter_by(id=asap_task_id).first()
        
        if not asap_task:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "ASAP Task not found"})
        
        asap_task.deleted = 1

        # Commit the changes to the database
        session.commit()

        # Close the session
        session.close()

        # Return success response
        return create_response(HTTPStatus.ACCEPTED, {"message": "ASAP Task deleted successfully"})
    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()