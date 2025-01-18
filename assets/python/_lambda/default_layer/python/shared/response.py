import json

class HTTPStatus:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Erlaube alle Origins (oder spezifische URL)
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # Zulässige Methoden
            "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Zulässige Header
        },
        "body": json.dumps(body, ensure_ascii=False)
    }
