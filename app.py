from flask import Flask, json, request
from datetime import datetime, timedelta
import time, requests, os
import dateutil.relativedelta

# functions in shared directory
from dashboard import *
from webhooks import *
from timeRetrieval import getTimeDiff
from employeeParse import *

# global list/dictionary
from globals import deviceHistory, NUMBER_EMPLOYEES

# init a flash web app
app = Flask(__name__)

# validate web server from meraki
@app.route('/', methods=['GET'])
def getValidator():
    return os.environ['SCANNING_VALIDATOR']


# receive location data
@app.route('/', methods=['POST'])
def getCmxJSON():
    global deviceCount
    cmxData = request.json
    # cmxdata = json.dumps(cmxdata, indent=2)
    APInfo = getAPInfo()
    APName = APInfo[0]['name']

    if cmxData['type'] == "BluetoothDevicesSeen":
        #print("\nNearby Bluetooth Tags:\n")
        btResponse = dashboardBT()
        setEmployeeInfo(cmxData, btResponse)
        currentEpoch = time.time()
        currentTime = datetime.fromtimestamp(currentEpoch)

        # reorganize mainUser to front of list
        deviceHistory['deviceList'] = sorted(deviceHistory['deviceList'], key = lambda i: 
            (i['isMainUser'], i['justArrived'], i['justLeft']), reverse = True)

        userHistory = deviceHistory['deviceList'][0]
    
        if userHistory['name'] is not None:
            selfMessage = ""

            # new or returning
            if userHistory['justArrived'] is True:
                #userHistory['isContinuous'] = True
                selfMessage = "You just entered the {}.".format(APName)
            # continuously in area
            elif userHistory['justArrived'] is False:
                selfMessage = "You are currently in the {}.".format(APName)
                
            print()
            print("{}".format(selfMessage))
                
        employeeCountMsg = getEmployeeCount()
        print()
        print("{}".format(employeeCountMsg))
        print()
        #sendMessage(employeeCountMsg)

        for employee in deviceHistory['deviceList'][1:]:
            employeeName = employee['name']
            
            if employeeName is not None:
                # employee currently in range
                if employee['isAway'] is False:
                    # new or returning
                    if employee['isContinuous'] is False:
                        nearbyEmployee = "{} just entered the {}".format(employeeName, APName)
                        timeDiff = getTimeDiff(employee['firstSeen'], currentTime) + " ago"
                    # continuously in area
                    elif employee['isContinuous'] is True:
                        #if employee['isMainUser'] is True:
                        #    selfMessage = "{} are in the {}".format(employeeName, APName)
                        #    print("{}".format(selfMessage))
                        #    continue
                        #else:
                        nearbyEmployee = "{} has been in the area for".format(employeeName)
                        timeDiff = getTimeDiff(employee['firstSeen'], currentTime)
                    
                    employeeMessage = nearbyEmployee + timeDiff + "."
                    #sendMessage(employeeMessage)
                    print("{}".format(employeeMessage))
                # employee out of range (employee['firstSeen'] is None)
                elif employee['isAway'] is True: #and employee['isMainUser'] is False:
                    # just left
                    if employee['justLeft'] is True:
                        employee['justLeft'] = False
                        awayEmployee = "{} just left the {}".format(employeeName, APName)
                    # previously gone
                    else:
                        awayEmployee = "{} is no longer in the area but was last nearby".format(employeeName)
                    
                    timeDiff = getTimeDiff(employee['lastSeen'], currentTime)
                    employeeMessage = awayEmployee + timeDiff + " ago."
                    # sendMessage(employeeMessage)
                    print("{}".format(employeeMessage))
    elif cmxData['type'] == "DevicesSeen":
        print("\nWiFi Devices Seen:\n")
        wifiResponse = dashboardWifi()
        setEmployeeInfo(cmxData, wifiResponse)
        currentEpoch = time.time()
        currentTime = datetime.fromtimestamp(currentEpoch)

        # reorganize mainUser to front of list
        deviceHistory['deviceList'] = sorted(deviceHistory['deviceList'], key = lambda i: 
            (i['isMainUser']), reverse = True) #''', i['justArrived'], i['justLeft']), reverse = True)

        userHistory = deviceHistory['deviceList'][1]

        if userHistory['isAway'] is False:
            selfMessage = ""

            # new or returning
            if userHistory['isContinuous'] is False:
                selfMessage = "You just entered the {}.".format(APName)
            # continuously in area
            elif userHistory['isContinuous'] is True:
                selfMessage = "You are currently in the {}.".format(APName)
            
            print()
            print("{}".format(selfMessage))
                
        employeeCountMsg = getEmployeeCount()
        print()
        print("{}".format(employeeCountMsg))
        print()
        #sendMessage(employeeCountMsg)

        for employee in deviceHistory['deviceList'][1:]:
            employeeName = employee['name']
            
            if employeeName is not None:
                # employee currently in range
                if employee['isAway'] is False:
                    # new or returning
                    if employee['isContinuous'] is False:
                        nearbyEmployee = "{} just entered the {}".format(employeeName, APName)
                        timeDiff = getTimeDiff(employee['firstSeen'], currentTime) + " ago"
                    # continuously in area
                    elif employee['isContinuous'] is True:
                        #if employee['isMainUser'] is True:
                        #    selfMessage = "{} are in the {}".format(employeeName, APName)
                        #    print("{}".format(selfMessage))
                        #    continue
                        #else:
                        nearbyEmployee = "{} has been in the area for".format(employeeName)
                        timeDiff = getTimeDiff(employee['firstSeen'], currentTime)
                    
                    employeeMessage = nearbyEmployee + timeDiff + "."
                    #sendMessage(employeeMessage)
                    print("{}".format(employeeMessage))
                # employee out of range (employee['firstSeen'] is None)
                elif employee['isAway'] is True: #and employee['isMainUser'] is False:
                    # just left
                    if employee['justLeft'] is True:
                        employee['justLeft'] = False
                        awayEmployee = "{} just left the {}".format(employeeName, APName)
                    # previously gone
                    else:
                        awayEmployee = "{} is no longer in the area but was last nearby".format(employeeName)
                    
                    timeDiff = getTimeDiff(employee['lastSeen'], currentTime)
                    employeeMessage = awayEmployee + timeDiff + " ago."
                    # sendMessage(employeeMessage)
                    print("{}".format(employeeMessage))
    else:
        print("Unknown Device 'type'")
    
    return "CMX POST Received"


if __name__ == '__main__':
    # run app
    app.run(port=8000, debug=False)