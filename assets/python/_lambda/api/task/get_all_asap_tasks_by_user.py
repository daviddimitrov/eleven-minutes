from orm.get_session import get_session
from orm.base import User, AsapTask
from dto.base import UserDTO, GetAsapTaskDTO
from shared.response import create_response, HTTPStatus
from dataclasses import asdict

def lambda_handler(event, context):
    session = get_session()
    try:
        user_id = event['pathParameters']['userId']

        user = session.query(User).filter_by(id=user_id).first()
        
        if user is None:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "User not found"})
        
        # Use the UserDTO to structure the user data
        user_dto = UserDTO(
            id=user.id,
            name=user.name,
            default_duration=user.default_duration
        )
        
        # Fetch tasks for the user
        asap_tasks = session.query(AsapTask).filter_by(user_id=user_id).filter_by(deleted=0).all()
        asap_task_dtos = []
        
        # Filter tasks based on the user’s default duration
        for asap_task in asap_tasks:
            # Convert to AsapTaskDTO
            asap_task_dto = GetAsapTaskDTO(
                id=asap_task.id,
                userId=UserDTO(id=asap_task.user_id, name=user.name, default_duration=user.default_duration),
                name=asap_task.name,
                deleted=asap_task.deleted
            )
            asap_task_dtos.append(asap_task_dto)
        
        # Return the response
        return create_response(HTTPStatus.OK, [asdict(asap_task_dto) for asap_task_dto in asap_task_dtos])

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()