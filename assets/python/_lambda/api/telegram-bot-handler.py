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
            task_list = ["<strong>{} {}</strong>\n📅 {}\n⏱️ {} Minuten\n☑️ /done_{}\n".format(task["name"], get_priority_emoji(task["priorityLevel"]["name"]), get_relative_date(task["dueDate"]), task["duration"], task["id"]) for task in tasks]
            reply = "<b>Heutige Aufgaben:</b>\n\n" + "\n".join(task_list)
    elif command == '/all':
        response = requests.get(
        f"https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/user/{chat_id}/tasks",
        timeout=30
        )
        tasks = response.json()
        print(tasks)

        if not tasks:
            reply = f"Du hast noch keine Aufgaben, {body["message"]["from"]["first_name"]}."
        else:
            task_list = ["<strong>{} {}</strong>\n📅 {}\n⏱️ {} Minuten\n☑️ /done_{}\n".format(task["name"], get_priority_emoji(task["priorityLevel"]["name"]), get_relative_date(task["dueDate"]), task["duration"], task["id"]) for task in tasks]
            reply = "<b>Deine Aufgaben:</b>\n\n" + "\n".join(task_list)
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
        reply = f"<b>Willkommen, {body["message"]["from"]["first_name"]}!</b> \n\nSchau, was heute zu tun ist: /today"
    
    # Telegram API aufrufen
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": reply, "parse_mode": "HTML"})

from datetime import datetime

def get_relative_date(date_str: str) -> str:
    try:
        due_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()
        delta = (due_date - today).days+1

        if delta == 0:
            return "heute"
        elif delta == 1:
            return "morgen"
        elif delta > 1:
            return f"in {delta} Tagen"
        elif delta == -1:
            return "gestern"
        else:
            return f"vor {-delta} Tagen"
    except ValueError:
        return "Ungültiges Datumsformat. Bitte ein Datum im Format 'YYYY-MM-DD' übergeben."

def get_priority_emoji(priority_name: str) -> str:
    match priority_name:
        case 'LOW':
            return "🟢"
        case 'MEDIUM':
            return "🟡"
        case 'HIGH':
            return "🔴"
        case 'ASAP':
            return "❗️"
        case _:
            return "⚪️"

def lambda_handler(event, context):
    """AWS Lambda Handler"""
    if event["httpMethod"] == "POST":
        process_message(event)
        return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
    return {"statusCode": 405, "body": "Method Not Allowed"}
