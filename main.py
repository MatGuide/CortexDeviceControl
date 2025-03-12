from CortexDeviceControl import DeviceControl
from dotenv import load_dotenv
import os

load_dotenv()

api_url = os.getenv("API_URL")
api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

server = os.getenv("EMAIL_SERVER_ADDRESS") 
port = os.getenv("EMAIL_SERVER_PORT")
sender = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")

interval = int(os.getenv("INTERVAL"))

receiver = [""]

if __name__ == "__main__":
    connection = DeviceControl(api_url, api_id, api_key)

    connection.get_device_violations(interval)
    report = connection.create_html_report()
    if report:
        connection.email_alert(server, port, sender, receiver, password)
