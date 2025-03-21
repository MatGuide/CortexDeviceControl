from CortexDeviceControl import DeviceControl
from dotenv import load_dotenv
from Teams import Teams
import os, json, asyncio


load_dotenv()

api_url = os.getenv("API_URL")
api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

server = os.getenv("EMAIL_SERVER_ADDRESS") 
port = os.getenv("EMAIL_SERVER_PORT")
sender = os.getenv("EMAIL_SENDER")
receivers = json.loads(os.getenv("EMAIL_RECEIVERS", "[]"))
password = os.getenv("EMAIL_PASSWORD")

interval = 1000000

app_id = os.getenv("APP_ID")
tenant_id = os.getenv("TENANT_ID")
client_secret = os.getenv("CLIENT_SECRET")

webhook_id = os.getenv("WEBHOOK_ID")


if __name__ == "__main__":
    connection = DeviceControl(api_url, api_id, api_key)
    violations = connection.get_device_violations(interval=interval)
    report = connection.create_html_report()

    if report:
        connection.email_alert(server, port, sender, receivers, password)

    teams = Teams(tenant_id, app_id, client_secret)
    teams.send_device_violation_to_channel(webhook_id, violations)
 

