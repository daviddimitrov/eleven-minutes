import json
import requests
from datetime import datetime, timedelta

TELEGRAM_TOKEN = "7847443833:AAFA5QtHAF7U8mAdn_Bgy52V0TNG7xSo5Ic"  # Ersetze durch deinen Token

def process_message(event):
    """Verarbeite eingehende Nachrichten und antworte."""
    body = json.loads(event["body"])
    if "message" not in body:  # Handle nur Nachrichten, keine anderen Updates
        return

    chat_id = body["message"]["chat"]["id"]
    message = body['message']
    
    if 'text' not in message:
        return

    text = body["message"]["text"]

    split_text = text.split("_")
    command = split_text[0]
    id = split_text[-1]

    if command == '/today':
        response = requests.get(
        f"https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/user/{chat_id}/tasks/today",
        timeout=30
        )
        tasks = response.json()
        print(tasks)

        if not tasks:
            reply = f"Alles geschafft!"
        else:
            task_list = ["• {} <i>({}min)</i> /done_{}".format(task["name"], task["duration"], task["id"]) for task in tasks]
            reply = "<b>Heutige Aufgaben:</b>\n" + "\n".join(task_list)
    elif command == '/done':    
        response = requests.get(
            f"https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/task/{id}",
            timeout=30
        )    
        task = response.json()
        
        end_date = datetime.today() + timedelta(days=task["rhythm"])
        string_date = end_date.strftime("%Y-%m-%d")

        # Update the dueDate field
        task['dueDate'] = string_date

        # Convert to JSON string with double-quoted property names
        formatted_task = json.dumps(task, ensure_ascii=False, indent=4)

        response = requests.put(
            f"https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/task/{id}",
            data=formatted_task,                         
        )

        reply = f"Du hast <b>{task['name']}</b> geschafft!"
    else:
        reply = f"<b>Willkommen!</b> \nSchau nach was du heute zu tun hast: /today"
    
    # Telegram API aufrufen
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": reply, "parse_mode": "HTML"})

def lambda_handler(event, context):
    """AWS Lambda Handler"""
    if event["httpMethod"] == "POST":
        process_message(event)
        return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
    return {"statusCode": 405, "body": "Method Not Allowed"}
