from shared.db_utils import fetch_one, fetch_all
from shared.error_handling import handle_error
from shared.response import create_response
import json

def lambda_handler(event, context):
    try:
        user_id = event['queryStringParameters'].get('user_id')
        user_data = fetch_one("""
            SELECT default_duration 
            FROM users 
            WHERE id = %s
            """,
            (user_id)
        )
        
        if user_data is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"})
            }
        
        default_duration = user_data["default_duration"]
        
        tasks = fetch_all("""
            SELECT id, name, duration, rhythm, due_date 
            FROM tasks 
            WHERE user_id = %s AND due_date <= CURDATE()
            ORDER BY priority_level ASC, due_date ASC, rhythm ASC
            """, 
            (user_id)
        )
        
        todays_tasks = []
        duration_today = 0
        
        for task in tasks:
            temp_duration = duration_today + task['duration']            
            if temp_duration <= default_duration:
                todays_tasks.append(
                    {
                        'name': task['name'],
                        'duration': task['duration']
                    }
                )  
                duration_today = temp_duration
        return create_response(200, todays_tasks)
    except Exception as e:
        error = handle_error(e)
        return create_response(500, error)
