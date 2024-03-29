from globals import mainUser, keyList, deviceHistory, deviceCount, NUMBER_EMPLOYEES
from datetime import datetime, timedelta
import time, requests, os, schedule, copy, dateutil.relativedelta


# functions in shared directory
from dashboard import dashboardBT, getAPInfo
from webhooks import sendMessage
from timeRetrieval import getTimeDiff

# compare seen Scanning MACs with connected Dashboard MACs
# assign nearby employee info
def setNearbyEmployees(dashboardResponse):
    global deviceCount
    global mainUser

    for client in dashboardResponse:
        # bluetooth
        if len(client['id']) == 18 and client['name'] is not None: 
            # first check if employee is in deviceHistory to prevent duplicate entries
            for employee in deviceHistory['deviceList']:
                # previously seen
                if employee['name'] == client['name']:
                    # returning employee
                    if employee['isAway'] is True:
                        employee['firstSeen'] = client['lastSeen']
                        employee['lastSeen'] = None
                        employee['isContinuous'] = False                        
                        employee['isAway'] = False
                        employee['justArrived'] = True
                        employee['justLeft'] = False
                        employee['hasChanged'] = True
                    # continuous sighting
                    else:
                        employee['lastSeen'] = None
                        employee['isContinuous'] = True
                        employee['isAway'] = False
                        employee['justArrived'] = False
                        employee['justLeft'] = False
                        employee['hasChanged'] = False

                    employee['updatedSeen'] = client['lastSeen']
                    break
                
            for employee in deviceHistory['deviceList']:
                # employee's intitial sighting
                if employee['name'] is None: 
                    if client['name'] == mainUser:
                        employee['isMainUser'] = True
                        employee['name'] = 'You'
                    else:
                        employee['isMainUser'] = False
                        employee['name'] = client['name'] 
                                                
                    employee['firstSeen'] = client['lastSeen']
                    employee['updatedSeen'] = client['lastSeen']
                    employee['lastSeen'] = None
                    employee['isContinuous'] = False
                    employee['isAway'] = False
                    employee['justArrived'] = True
                    employee['justLeft'] = False
                    employee['hasChanged'] = True
                    break
        # wifi
        elif len(client['id']) == 7: 
            deviceCount += 1

            # first check if employee is in deviceHistory to prevent duplicate entries
            for employee in deviceHistory['deviceList']:
                # previously seen
                if employee['name'] == client['description']:
                    # returning employee
                    if employee['isAway'] is True:
                        employee['firstSeen'] = client['lastSeen']
                        employee['lastSeen'] = None
                        employee['isAway'] = False
                        employee['justArrived'] = True
                        employee['hasChanged'] = True
                    # continuous sighting
                    else:
                        employee['isContinuous'] = True
                        employee['justArrived'] = False
                        employee['hasChanged'] = False

                    employee['updatedSeen'] = client['lastSeen']
                    break
                # employee's intitial sighting
                elif employee['name'] is None: 
                    if client['description'] == mainUser:
                        employee['isMainUser'] = True
                        employee['name'] = 'You'
                    else:
                        employee['isMainUser'] = False
                        employee['name'] = client['description'] 
                                                    
                    employee['firstSeen'] = client['lastSeen']
                    employee['updatedSeen'] = client['lastSeen']
                    employee['isContinuous'] = False
                    employee['isAway'] = False
                    employee['justArrived'] = True
                    employee['hasChanged'] = True
                    break
                else:
                    continue
        else:
            continue

# assign away employee info    
def setAwayEmployees():
    seq = [x['updatedSeen'] for x in deviceHistory['deviceList']]
    maxTime = max(seq)

    # compare last in range employees
    # employees with lower updatedSeen times are away
    for employee in deviceHistory['deviceList']:
        if employee['isMainUser'] is False and employee['updatedSeen'] < maxTime:
            employee['firstSeen'] = None
            employee['lastSeen'] = employee['updatedSeen']
            employee['isContinuous'] = False
            employee['isAway'] = True
            employee['justArrived'] = False
            employee['justLeft'] = True
            employee['hasChanged'] = True


def setEmployeeCount():
    global deviceCount

    seq = [x['updatedSeen'] for x in deviceHistory['deviceList']]
    maxTime = max(seq)

    for employee in deviceHistory['deviceList']:
        if employee['isMainUser'] is True:
            deviceCount += 1
        elif employee['updatedSeen'] == maxTime:
            deviceCount += 1

# set both nearby and away employees
# create employee count message
def setEmployeeInfo(dashboardResponse):
    global deviceCount
    deviceCount = 0

    setNearbyEmployees(dashboardResponse)    
    setAwayEmployees()
    setEmployeeCount()


def getEmployeeCount():
    employeeCountMsg = ""

    if deviceCount >= NUMBER_EMPLOYEES:
        employeeCountMsg += "COVID WARNING! AREA AT CAPACITY!\n"
    else:
        employeeCountMsg += "Area at safe occupancy. Remember to social distance!\n"

    if deviceCount == 2:
        grammarInsert = " is"
    else:
        grammarInsert = "s are"
        
    employeeCountMsg += "{} other employee{} currently around you.".format(str(deviceCount - 1), grammarInsert)

    return employeeCountMsg

def getInfo():
    responseBT = dashboardBT()
    setEmployeeInfo(responseBT)
    APInfo = getAPInfo()
    APName = APInfo[0]['name']
    currentEpoch = time.time()
    currentTime = datetime.fromtimestamp(currentEpoch)

    print("\n------------------------------------------------------")
    print(currentTime)

    # reorganize mainUser to front of list
    deviceHistory['deviceList'] = sorted(deviceHistory['deviceList'], key = lambda i: 
        (i['isMainUser'], i['justArrived'], i['justLeft']), reverse = True)

    user = deviceHistory['deviceList'][0]

    if user['name'] is not None:        
        print()
        selfMessage = ""

        # new or returning
        if user['justArrived'] is True:
            user['justArrived'] = False
            selfMessage = "You just entered the {}.".format(APName)
        # continuously in area
        elif user['justArrived'] is False:
            selfMessage = "You are currently in the {}.".format(APName)
            
        print("{}".format(selfMessage))
        sendMessage(selfMessage)
            
    employeeCountMsg = getEmployeeCount()
    print()
    print("{}".format(employeeCountMsg))
    print()
    sendMessage(employeeCountMsg)

    for employee in deviceHistory['deviceList'][1:]:
        employeeName = employee['name']

        if employeeName is not None:
            # employee currently in range
            if employee['isAway'] is False:
                # new or returning
                if employee['justArrived'] is True:
                    nearbyEmployee = "{} just entered the {}".format(employeeName, APName)
                    timeDiff = getTimeDiff(employee['firstSeen'], currentTime) + " ago"
                # continuously in area
                elif employee['isContinuous'] is True:
                    nearbyEmployee = "{} has been in the area for".format(employeeName)
                    timeDiff = getTimeDiff(employee['firstSeen'], currentTime)

                employeeMessage = nearbyEmployee + timeDiff + "."
                sendMessage(employeeMessage)
                print("{}".format(employeeMessage))
            # employee out of range (employee['firstSeen'] is None)
            elif employee['isAway'] is True:
                # just left
                if employee['justLeft'] is True:
                    awayEmployee = "{} left the area".format(employeeName)
                    employee['justLeft'] = False
                # previously gone
                else:
                    awayEmployee = "{} is no longer in the area but was last nearby".format(employeeName)
                
                timeDiff = getTimeDiff(employee['lastSeen'], currentTime)
                employeeMessage = awayEmployee + timeDiff + " ago."
                sendMessage(employeeMessage)
                print("{}".format(employeeMessage))