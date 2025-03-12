from CortexDeviceControl import DeviceControl
from dotenv import load_dotenv
import os

load_dotenv()

api_url = os.getenv("API_URL")
api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

if __name__ == "__main__":
    connection = DeviceControl(api_url, api_id, api_key)
    connection.get_device_violations()
    connection.create_html_report()
