from CortexDeviceControl import DeviceControl
from Teams import Teams
from dotenv import load_dotenv
import os, json

load_dotenv()

api_url = os.getenv("API_URL")
api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

server = os.getenv("EMAIL_SERVER_ADDRESS") 
port = os.getenv("EMAIL_SERVER_PORT")
sender = os.getenv("EMAIL_SENDER")
receivers = json.loads(os.getenv("EMAIL_RECEIVERS", "[]"))
password = os.getenv("EMAIL_PASSWORD")

interval = int(os.getenv("INTERVAL"))

client_id = os.getenv("CLIENT_ID")
username = os.getenv("USERNAME")
teams_password = os.getenv("PASSWORD")


if __name__ == "__main__":
    connection = DeviceControl(api_url, api_id, api_key)
    violations = connection.get_device_violations()
    report = connection.create_html_report()

    teams = Teams(client_id, username, teams_password)
    teams.send_teams_alert(violations)
    teams.send_teams_alert_to_team("Cortex XSIAM", "Cortex XSIAM")
    if report:
        connection.email_alert(server, port, sender, receivers, password)
