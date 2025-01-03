import mysql.connector
import json

def lambda_handler(event, context):
    # Hardcodierte Verbindungsdaten für die MySQL-Datenbank
    host = 'eleven-minutes-eleven-minutes.b.aivencloud.com'
    user = ''
    password = ''  # Ersetze dies mit deinem tatsächlichen Passwort
    database = 'defaultdb'
    port = 12493
    
    # Extrahiere user_id aus dem Event (z. B. aus dem Query-String)
    user_id = event['queryStringParameters'].get('user_id')

    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing user_id in query parameters.'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # Verbindung zur MySQL-Datenbank herstellen
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl_disabled=False  # SSL-Mode aktivieren
        )
        
        cursor = connection.cursor()

        # Abfrage, um das erste Ergebnis für eine bestimmte user_id zu holen
        query = "SELECT * FROM command_history WHERE user_id = %s LIMIT 1;"
        cursor.execute(query, (user_id,))

        # Ein Ergebnis abrufen
        result = cursor.fetchone()

        if result:
            # Die Spaltennamen der Tabelle abholen, um sie zusammen mit den Daten zurückzugeben
            column_names = [desc[0] for desc in cursor.description]
            
            # Ergebnis als Dictionary formatieren
            command_history = dict(zip(column_names, result))

            # Verbindung schließen
            cursor.close()
            connection.close()

            # Erfolgreiche Rückgabe mit dem Ergebnis
            return {
                'statusCode': 200,
                'body': json.dumps(command_history),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            # Kein Ergebnis gefunden
            cursor.close()
            connection.close()
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': f'No command history found for user_id {user_id}.'
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

    except mysql.connector.Error as err:
        # Fehlerbehandlung
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Database error occurred.',
                'error': str(err)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
