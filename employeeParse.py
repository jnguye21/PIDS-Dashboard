from globals import mainUser, keyList, deviceHistory, deviceCount, NUMBER_EMPLOYEES

# compare seen Scanning MACs with connected Dashboard MACs
# assign nearby employee info
def setNearbyEmployees(dashboardResponse):
    global deviceCount
    global mainUser

    for client in dashboardResponse:
        # bluetooth
        if len(client['id']) == 18 and client['name'] is not None: 
            #deviceCount += 1
            # first check if employee is in deviceHistory to prevent duplicate entries
            for employee in deviceHistory['deviceList']:
                # previously seen
                if employee['name'] == client['name']:
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
                        employee['isAway'] = False
                        employee['justArrived'] = False
                        employee['hasChanged'] = False

                    employee['updatedSeen'] = client['lastSeen']
                    #print('{}'.format(client['name']))
                    break
                #else:
                #    continue
                
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
                    employee['isContinuous'] = False
                    employee['isAway'] = False
                    employee['justArrived'] = True
                    employee['hasChanged'] = True
                    break
                #else:
                #    continue
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
                    #print('{}'.format(client['name']))
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
    # compare last in range employees
    # employees with lower updatedSeen times are 
    for employee1 in deviceHistory['deviceList']:
        if employee1['isMainUser'] is True:
            break
        if employee1['isAway'] is False and employee1['isMainUser'] is False:
            for employee2 in deviceHistory['deviceList']:
                if employee1['name'] != employee2['name'] and employee2['isAway'] is False:
                    if employee1['updatedSeen'] < employee2['updatedSeen']:
                        employee1['firstSeen'] = None
                        employee1['lastSeen'] = employee1['updatedSeen']
                        employee1['isContinuous'] = False
                        employee1['isAway'] = True
                        employee1['justLeft'] = True
                        employee1['hasChanged'] = True
                        break
                    elif employee2['updatedSeen'] < employee1['updatedSeen']:
                        employee2['firstSeen'] = None
                        employee2['lastSeen'] = employee2['updatedSeen']
                        employee2['isContinuous'] = False
                        employee2['isAway'] = True
                        employee2['justLeft'] = True
                        employee2['hasChanged'] = True
                        break
                    else:
                        continue

def setEmployeeCount():
    global deviceCount

    seq = [x['updatedSeen'] for x in deviceHistory['deviceList']]
    maxTime = max(seq)

    for employee in deviceHistory['deviceList']:
        if employee['name'] == mainUser:
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
        
    employeeCountMsg += "{} other employee{} currently in the area.".format(str(deviceCount - 1), grammarInsert)

    return employeeCountMsg