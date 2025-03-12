import requests
import json

class DeviceControl:

    def __init__(self, url, api_id, api_key):
        self.url = url
        self.api_id = api_id
        self.api_key = api_key

        self.headers = {
            "x-xdr-auth-id": str(self.api_id),
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.payload = {}
        self.sufix = ""

    def get_device_violations(self):
        self.sufix = "/device_control/get_violations" 
        self.payload = { "request_data": {} }

        request_url = self.url + self.sufix
        json_report = {}

        try:
            response = requests.post(request_url, json=self.payload, headers=self.headers)
        except Exception as e:
            print(f"Error occured {e}.")
        else:
            violations = response.json()["reply"]["violations"]
            for violation in violations:
                json_report.append(violation)
                test = json.dump(json_report, indent=4)
            print(test)
        
    # def email_alert(self):
    #     pass


