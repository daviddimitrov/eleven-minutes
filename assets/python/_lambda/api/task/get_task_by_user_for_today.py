from orm.get_session import get_session
from orm.base import User, Task, PriorityLevel
from dto.base import UserDTO, TaskDTO, PriorityLevelDTO, GetTaskDTO
from shared.response import create_response, HTTPStatus
from dataclasses import asdict
from sqlalchemy import func


def lambda_handler(event, context):
    session = get_session()
    try:
        user_id = event['queryStringParameters'].get('user_id')
        
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
        tasks = session.query(Task).filter_by(user_id=user_id).filter(Task.due_date <= func.curdate()).all()
        
        todays_tasks = []
        duration_today = 0
        
        # Filter tasks based on the user’s default duration
        for task in tasks:
            # Convert to TaskDTO
            task_dto = TaskDTO(
                id=task.id,
                user_id=task.user_id,
                priority_level_id=task.priority_level_id,
                name=task.name,
                duration=task.duration,
                due_date=task.due_date.isoformat(),
                rhythm=task.rhythm
            )
            
            temp_duration = duration_today + task_dto.duration            
            if temp_duration <= user_dto.default_duration:
                todays_tasks.append(task_dto)
                duration_today = temp_duration
        
        # Return the response
        return create_response(HTTPStatus.OK, [asdict(task) for task in todays_tasks])

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()