from datetime import date
from orm.get_session import get_session
from orm.base import User, Task, PriorityLevel
from dto.base import UserDTO, TaskDTO, PriorityLevelDTO, GetTaskDTO
from shared.response import create_response, HTTPStatus
from dataclasses import asdict


def lambda_handler(event, context):
    """
    AWS Lambda handler for testing database operations with DTOs.
    """
    session = get_session()
    try:
        # Extract data from the event
        user_id = event.get("user_id", "user123")
        user_name = event.get("name", "John Doe")
        default_duration = event.get("default_duration", 60)

        # Fetch or create a UserDTO
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, name=user_name, default_duration=default_duration)
            session.add(user)
            session.commit()
        user_dto = UserDTO(id=user.id, name=user.name, default_duration=user.default_duration)

        # Fetch or create a PriorityLevelDTO
        priority_level = session.query(PriorityLevel).filter_by(name="High Priority").first()
        if not priority_level:
            priority_level = PriorityLevel(name="High Priority")
            session.add(priority_level)
            session.commit()
        priority_level_dto = PriorityLevelDTO(id=priority_level.id, name=priority_level.name)

        # Create a Task and convert to TaskDTO
        task = Task(
            user_id=user.id,
            priority_level_id=priority_level.id,
            name="Complete report",
            duration=120,
            due_date=date(2025, 1, 10),
            rhythm=7
        )
        session.add(task)
        session.commit()

        # Convert due_date to string (ISO format)
        task_dto = TaskDTO(
            id=task.id,
            user_id=task.user_id,
            priority_level_id=task.priority_level_id,
            name=task.name,
            duration=task.duration,
            due_date=task.due_date.isoformat(),  # Convert date to string
            rhythm=task.rhythm
        )

        # Convert Task to GetTaskDTO (with nested UserDTO and PriorityLevelDTO)
        get_task_dto = GetTaskDTO(
            id=task.id,
            userId=user_dto,  # Nested UserDTO
            priorityLevel=priority_level_dto,  # Nested PriorityLevelDTO
            name=task.name,
            duration=task.duration,
            dueDate=task.due_date.isoformat(),  # Convert date to string
            rhythm=task.rhythm
        )

        # Query and return the user's tasks as GetTaskDTOs
        user_tasks = session.query(Task).filter_by(user_id=user.id).all()
        tasks_output = [
            GetTaskDTO(
                id=task.id,
                userId=UserDTO(id=task.user_id, name=user.name, default_duration=user.default_duration),
                priorityLevel=PriorityLevelDTO(id=task.priority_level_id, name=priority_level.name),
                name=task.name,
                duration=task.duration,
                dueDate=task.due_date.isoformat(),  # Convert date to string
                rhythm=task.rhythm
            )
            for task in user_tasks
        ]

        return create_response(HTTPStatus.OK, [asdict(task) for task in tasks_output])
    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
        session.close()
