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
        task_id = event['pathParameters']['taskId']

        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "Task not found"})
        
        user = session.query(User).filter_by(id=task.user_id).first()
        priority_level = session.query(PriorityLevel).filter_by(id=task.priority_level_id).first()

        task_dto = GetTaskDTO(
                id=task.id,
                userId=UserDTO(id=user.id, name=user.name, default_duration=user.default_duration),
                priorityLevel=PriorityLevelDTO(id=priority_level.id, name=priority_level.name),
                name=task.name,
                duration=task.duration,
                dueDate=task.due_date.isoformat(),
                rhythm=task.rhythm
            )
        
        # Return the response
        return create_response(HTTPStatus.OK, asdict(task_dto))

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()