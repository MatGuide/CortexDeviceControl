import requests
import json
import smtplib
import ssl
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
 
        past_time = int((datetime.utcnow() - timedelta(minutes=interval)).timestamp() * 1000)

        self.sufix = "/device_control/get_violations" 

        self.payload = {
            "request_data": {
                "filters": [
                    {
                        "field": "timestamp",
                        "operator": "gte",
                        "value": past_time
                    }
                ]
            }
        }
        

        request_url = self.url + self.sufix
        json_report = []

        try:
            response = requests.post(request_url, json=self.payload, headers=self.headers)
        except Exception as e:
            print(f"Error occured {e}.")
        else:
            violations = response.json()["reply"]["violations"]

            if violations != []:   
                try:
                    with open("violations.json", "w", encoding="utf-8") as file:
                        json.dump(violations, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Error occured {e}.")
            else:
                with open("violations.json", "w") as file:
                    json.dump({}, file)
            

    def create_html_report(self):
        
        data = []

        html_template = """
        <!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Raport</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                table { width: 100%%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Raport</h1>
            <p>Data wygenerowania: {{ date }}</p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Time</th>
                    <th>Hostname</th>
                    <th>Username</th>
                    <th>Vendor</th>
                    <th>Product</th>
                    <th>Device SN</th>
                </tr>
                {% for item in data %}
                <tr>
                    <td>{{ item.violation_id }}</td>
                    <td>{{ item.timestamp }}</td>
                    <td>{{ item.hostname }}</td>
                    <td>{{ item.username }}</td>
                    <td>{{ item.vendor }}</td>
                    <td>{{ item.product }}</td>
                    <td>{{ item.serial }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """

        with open('violations.json', 'r') as file:
            violations = json.load(file)
        
        if violations != {}: 
            for violation in violations:
                timestamp = datetime.utcfromtimestamp(violation["timestamp"]/1000).strftime('%Y-%m-%d %H:%M:%S')            
                data.append({"violation_id": violation["violation_id"], "timestamp": timestamp, "hostname": violation["hostname"], "username": violation["username"], \
                "vendor": violation["vendor"], "product": violation["product"], "serial": violation["serial"]})
            
            template = Template(html_template)
            html_report = template.render(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data=data)

            with open("report.html", "w") as file:
                file.write(html_report)

            return True

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

        message.attach(MIMEText(text, "html"))

        with smtplib.SMTP(server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            
