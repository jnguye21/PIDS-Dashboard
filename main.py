#from flask import Flask, json, request
from datetime import datetime, timedelta
import schedule, sys, copy
import time, requests, os
import dateutil.relativedelta

# functions in shared directory
from dashboard import *
from webhooks import *
from timeRetrieval import getTimeDiff
from employeeParse import *

# global list/dictionary
from globals import deviceHistory, NUMBER_EMPLOYEES

def job():
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
    
    print()
    print(user)
    print()

    if user['name'] is not None:        
        selfMessage = ""

        # new or returning
        if user['justArrived'] is True:
            user['justArrived'] = False
            selfMessage = "You just entered the {}.".format(APName)
        # continuously in area
        elif user['justArrived'] is False:
            selfMessage = "You are currently in the {}.".format(APName)
            
        print("{}".format(selfMessage))
            
    employeeCountMsg = getEmployeeCount()
    print()
    print("{}".format(employeeCountMsg))
    print()
    #sendMessage(employeeCountMsg)

    deviceHistory2 = copy.deepcopy(deviceHistory)

    for employee in deviceHistory2['deviceList'][1:]:
        employeeName = employee['name']
        empTime = employee['updatedSeen']
        print(empTime)

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

def main():    
    try:
        schedule.every().minute.at(":00").do(job)
    
        while True:
            schedule.run_pending()
            time.sleep(1)    
    
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()