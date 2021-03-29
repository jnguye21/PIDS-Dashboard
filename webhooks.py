import requests
import os

def sendMessage(message):
    url = os.environ['TEAMS_WEBHOOK_URL']
    myObj = {'text': message}

    requests.post(url, data = myObj)