import json
import requests

TELEGRAM_TOKEN = ""  # Ersetze durch deinen Token

def process_message(event):
    """Verarbeite eingehende Nachrichten und antworte."""
    body = json.loads(event["body"])
    if "message" not in body:  # Handle nur Nachrichten, keine anderen Updates
        return

    chat_id = body["message"]["chat"]["id"]
    text = body["message"]["text"]
    print("chat_id")
    print(chat_id)
    print("text")
    print(text)

    split_text = text.split("_")
    command = split_text[0]
    id = split_text[-1]

    print("command")
    print(command)
    print("id")
    print(id)

    if command == '/delete':
        reply = f"Task mit der ID: {id} gelöscht."
    elif command == '/api':
        response = requests.get(
        'https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/command_history',
        params={
            "user_id": chat_id
        },
        timeout=30,
        )
        reply = f"API antwortet mit: {response.status_code}"
    elif command == '/today':
        tasks = requests.get(
        'https://n6vigzrqtg.execute-api.eu-central-1.amazonaws.com/dev/task/today',
        params={
            "user_id": chat_id
        },
        timeout=30,
        )

        if not tasks.text:
            reply = f"Alles geschafft!"
        
        task_list = ["- {} ({} Minuten)".format(task["name"], task["duration"]) for task in tasks.json()]
        
        reply = "Heutige Aufgaben:\n" + "\n".join(task_list)
    else:
        reply = f"Hallo! Du hast geschrieben: {text}. \n\n Das hier ist deine chat_id: {chat_id}. \n\n Schicke einen neuen Command: \n/delete_task_123 \n/delete_task_456 \n/delete_task_789 "
    
    # Telegram API aufrufen
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": reply})

def lambda_handler(event, context):
    """AWS Lambda Handler"""
    if event["httpMethod"] == "POST":
        process_message(event)
        return {"statusCode": 200, "body": json.dumps({"message": "OK"})}
    return {"statusCode": 405, "body": "Method Not Allowed"}
