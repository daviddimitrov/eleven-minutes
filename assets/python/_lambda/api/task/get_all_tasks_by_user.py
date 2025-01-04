from orm.get_session import get_session
from orm.base import User, Task, PriorityLevel
from dto.base import UserDTO, TaskDTO, PriorityLevelDTO, GetTaskDTO
from shared.response import create_response, HTTPStatus
from shared.validation import validate_input
from dataclasses import asdict
from sqlalchemy import func


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
        tasks = session.query(Task).filter_by(user_id=user_id).order_by(
            Task.due_date.asc(),  # Sort by due_date in descending order
            Task.priority_level_id.asc(),  # Sort by priority_level_id in ascending order
            Task.rhythm.asc()  # Sort by rhythm in ascending order
        ).all()
        task_dtos = []
        
        # Filter tasks based on the user’s default duration
        for task in tasks:
            priority_level = session.query(PriorityLevel).filter_by(id=task.priority_level_id).first()
            # Convert to TaskDTO
            task_dto = GetTaskDTO(
                id=task.id,
                userId=UserDTO(id=task.user_id, name=user.name, default_duration=user.default_duration),
                priorityLevel=PriorityLevelDTO(id=task.priority_level_id, name=priority_level.name),
                name=task.name,
                duration=task.duration,
                dueDate=task.due_date.isoformat(),
                rhythm=task.rhythm
            )
            task_dtos.append(task_dto)
        
        # Return the response
        return create_response(HTTPStatus.OK, [asdict(task_dto) for task_dto in task_dtos])

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()