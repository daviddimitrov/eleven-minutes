from orm.get_session import get_session
from orm.base import User, Task
from shared.response import create_response, HTTPStatus
from sqlalchemy import func


def lambda_handler(event, context):
    session = get_session()
    try:
        user_id = event['pathParameters']['userId']

        user = session.query(User).filter_by(id=user_id).first()
        
        if user is None:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "User not found"})
        
        session.query(Task).filter(Task.user_id == user_id).update({"today": 0})
        session.commit()
        
        # Fetch tasks for the user
        tasks = session.query(Task).filter_by(user_id=user_id).filter(Task.due_date <= func.curdate()).order_by(
            Task.priority_level_id.asc(),  # Sort by priority_level_id in ascending order
            Task.due_date.asc(),  # Sort by due_date in descending order
            Task.rhythm.asc()  # Sort by rhythm in ascending order
        ).all()
        duration_today = 0
        
        # Filter tasks based on the user’s default duration
        for task in tasks:
            temp_duration = duration_today + task.duration            
            if temp_duration <= user.default_duration:
                duration_today = temp_duration
                task.today = 1
                session.commit()

        session.close()        
        # Return the response
        return create_response(HTTPStatus.ACCEPTED, {"message": "Collected today's tasks successfully"})

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()