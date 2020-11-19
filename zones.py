myDict = {
    'deviceList': [
        {
            'name': None,
           'firstSeen': None,
           'updatedSeen': None,
           'lastSeen': None,
           'isContinuous': None,
           'isAway': None,  
           'zone': None, # 1 or 2
           'hasChanged': None
        }
    ]
}

def setZone(employeeDict, rssi):
    for emp in employeeDict['deviceList']:
        # within 20 ft
        if rssi >= -85:
            emp['zone'] = 1
        #outside 20 ft
        else:
            emp['zone'] = 2 

    return employeeDict

test1 = setZone(myDict, 75)
print(test1)