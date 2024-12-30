import mysql.connector
import json

# Lambda Handler
def lambda_handler(event, context):
    # Verbindungsdaten zur MySQL-Datenbank
    db_host = "eleven-minutes-eleven-minutes.b.aivencloud.com"
    db_user = ""
    db_password = ""  # Dein Passwort hier
    db_name = "defaultdb"
    port = 12493

    # Benutzer-ID, die in der Anfrage erwartet wird (von API Gateway)
    user_id = event['queryStringParameters'].get('user_id')

    
    try:
        # Verbindung zur MySQL-Datenbank herstellen
        db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=port,
            ssl_disabled=False 
        )
        
        cursor = db.cursor(dictionary=True)
        
        # Abfrage, um die Standarddauer des Benutzers zu bekommen
        cursor.execute("""
            SELECT default_duration 
            FROM users 
            WHERE id = %s
        """, (user_id,))
        user_data = cursor.fetchone()
        
        if user_data is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"})
            }
        
        default_duration = user_data["default_duration"]
        
        # Abfrage für die Aufgaben, die heute oder in der Vergangenheit fällig sind
        cursor.execute("""
            SELECT id, name, duration, rhythm, due_date 
            FROM tasks 
            WHERE user_id = %s AND due_date <= CURDATE()
            ORDER BY priority_level ASC, due_date ASC, rhythm ASC
        """, (user_id,))
        
        # Alle Aufgaben für den Benutzer holen
        tasks = cursor.fetchall()
        
        # Liste für Aufgaben, die wir heute erledigen wollen
        todays_tasks = []
        
        # Kumulierte Dauer initialisieren
        duration_today = 0
        
        # Schleife über alle Aufgaben
        for task in tasks:
            temp_duration = duration_today + task['duration']
            
            # Prüfen, ob die kumulierte Dauer den Default-Wert überschreiten würde
            if temp_duration <= default_duration:
                todays_tasks.append(
                    {
                        'name': task['name'],
                        'duration': task['duration']
                    }
                    )  # Aufgabe zur Liste hinzufügen
                duration_today = temp_duration  # Kumulierte Dauer aktualisieren
        
        # Verbindung schließen
        cursor.close()
        db.close()
        
        # Ergebnis zurückgeben
        return {
            "statusCode": 200,
            "body": json.dumps(todays_tasks, ensure_ascii=False)
        }
    
    except mysql.connector.Error as err:
        # Fehlerbehandlung bei Datenbankfehlern
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Database error: {err}"})
        }
    except Exception as e:
        # Fehlerbehandlung für unerwartete Fehler
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
