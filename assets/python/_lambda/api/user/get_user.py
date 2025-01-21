from orm.get_session import get_session
from orm.base import User
from dto.base import UserDTO
from shared.response import create_response, HTTPStatus
from dataclasses import asdict


def lambda_handler(event, context):
    session = get_session()
    try:
        user_name = event["queryStringParameters"]['user_name']

        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            return create_response(HTTPStatus.NOT_FOUND, {"message": "User not found"})

        user_dto = UserDTO(
                id=user.id,
                name=user.name,
                default_duration=user.default_duration
        )

        # Return the response
        return create_response(HTTPStatus.OK, asdict(user_dto))

    
    except Exception as e:
        session.rollback()
        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"message": "An error occurred", "error": str(e)})
    finally:
            session.close()