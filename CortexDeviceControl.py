import requests
import json
import smtplib
import time
from jinja2 import Template
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

    def get_device_violations(self, interval):

        new_time = datetime.now() - timedelta(minutes=interval)
        new_time_ms = int(new_time.timestamp() * 1000)

        self.sufix = "/device_control/get_violations" 

        self.payload = {
            "request_data": {
                "filters": [
                    {
                        "field": "timestamp",
                        "operator": "gte",
                        "value": new_time_ms
                    }
                ]
            }
        }

        request_url = self.url + self.sufix

        try:
            response = requests.post(request_url, json=self.payload, headers=self.headers)
        except Exception as e:
            print(f"Error occured {e}.")

        try:
            if "err_code" not in str(response.json()):
                violations = response.json()["reply"]["violations"]
                if violations != []:
                    
                    try:
                        with open("violations.json", "w", encoding="utf-8") as file:
                            json.dump(violations, file, ensure_ascii=False, indent=4)
                            return violations
                    except Exception as e:
                        print(f"Error occured {e}.")
                else:
                    with open("violations.json", "w") as file:
                        json.dump({}, file)
        except Exception as e:
            (f"Error occured, {response.json()}")

    def create_html_report(self):
        
        data = []

        with open("template.html", "r") as template:
            html_template = template.read()
        try:
            with open('violations.json', 'r') as file:
                violations = json.load(file)

                if violations != {}:
                    for violation in violations:
                        timestamp =  datetime.fromtimestamp(violation["timestamp"]/1000).strftime('%Y-%m-%d %H:%M:%S')     
                        data.append({"violation_id": violation["violation_id"], "timestamp": timestamp, "hostname": violation["hostname"], "username": violation["username"], \
                        "vendor": violation["vendor"], "product": violation["product"], "serial": violation["serial"]})
                
                    template = Template(html_template)
                    date = datetime.now() + timedelta(hours=1)
                    date = date.strftime('%Y-%m-%d %H:%M:%S')
                    
                    html_report = template.render(date=date, data=data)
                    
                    with open("report.html", "w") as file:
                        file.write(html_report)

                    return True
                
            
        except FileNotFoundError as e:
            print(f"File not exists {e}")
        

    def email_alert(self, server, port, sender_email, receiver_email, password):

        try:
            with open("report.html", "r") as file:
                text = file.read()
        except Exception as e:
            print(f"Error occured {e}.")


        message = MIMEMultipart()
        message["Subject"] = "Device violation detected"
        message["From"] = sender_email
        message["To"] = ",".join(receiver_email)
        message.add_header("Content-Type", "text/html")

        report = MIMEText(text, "html")

        message.attach(report)

        with smtplib.SMTP(server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
    

