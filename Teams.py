import requests
import msal
from msgraph import GraphServiceClient

class Teams:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]

        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_access_token(self):

        app = msal.ConfidentialClientApplication(
            client_id=self.client_id, 
            authority=self.auth_url,
            client_credential=self.client_secret,
            token_cache=None
        )

        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))

    def send_device_violation_to_channel(self, webhook_id, violations):
        
        message = ""

        template = {
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                "type": "Container",
                "items": [],
                "height": "stretch",
                "style": "attention"
                },
                {
                "type": "TextBlock",
                "text": "🔥 Krytyczny błąd!",
                "weight": "Bolder",
                "size": "Large",
                "wrap": True
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
            }

        if message != None:
            for violation in violations:
                template['body'][1]['text'] = f"📢 **Device violation detected** 📢**ID: **{violation['violation_id']}\n\n**Timestamp: **{violation['timestamp']}\n\n**Hostname: **{violation['hostname']}\n\n**IP: **{violation['ip']}\n\n**Username: **{violation['username']}\n\n**Type: **{violation['type']}\n\n**Product: **{violation['product']}"

                response = requests.post(f"https://webhookbot.c-toss.com/api/bot/webhooks/{webhook_id}", headers=self.headers, json=template)

        print(response)
        
