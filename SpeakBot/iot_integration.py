import requests

class IoTIntegration:
    def __init__(self):
        self.device_url = "http://device-url.com"

    def interact_with_device(self, command):
        requests.post(self.device_url, json={"command": command})