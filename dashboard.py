import os
import requests, json

# dashboard call for connected WiFi clients
def dashboardWifi():
    url = os.environ['MERAKI_URL_WIFI']

    payload = {}
    headers = {
        'X-Cisco-Meraki-API-Key': os.environ['MERAKI_DASHBOARD_API_KEY']
    }

    responseWifi = requests.request("GET", url, headers=headers, data = payload)
    responseWifi = json.loads(responseWifi.text.encode('utf8'))
    return responseWifi

# dashboard call for connected BT clients
def dashboardBT():
    url = os.environ['MERAKI_URL_BT']

    payload = {}
    headers = {
        'X-Cisco-Meraki-API-Key': os.environ['MERAKI_DASHBOARD_API_KEY']
    }

    responseBT = requests.request("GET", url, headers=headers, data = payload)
    responseBT = json.loads(responseBT.text.encode('utf8'))
    return responseBT    

def getAPInfo():
    url = os.environ['MERAKI_URL_AP']

    payload = {}
    headers = {
        'X-Cisco-Meraki-API-Key': os.environ['MERAKI_DASHBOARD_API_KEY']
    }

    responseAP = requests.request("GET", url, headers=headers, data = payload)
    responseAP = json.loads(responseAP.text.encode('utf8'))
    return responseAP

