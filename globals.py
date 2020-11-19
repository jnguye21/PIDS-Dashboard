# Global data to be shared among directory

mainUser = 'Andrea'

NUMBER_EMPLOYEES = 4

keyList = ['isMainUser', 'name', 'firstSeen', 'updatedSeen', 'lastSeen', 'isContinuous', 
            'isAway', 'justArrived', 'justLeft', 'hasChanged']
deviceHistory = {'deviceList': [{key: None for key in keyList} for number in range(NUMBER_EMPLOYEES)]}

for i in deviceHistory['deviceList']:
    i['isMainUser'] = False
    i['justArrived'] = False
    i['justLeft'] = False

deviceCount = 0

# deviceHistory = {
#       'deviceList': [
#           {
#               'isMainUser': <bool>
#               'name': <string>,
#               'firstSeen': <int>,
#               'updatedSeen': <int>,
#               'lastSeen': <int>,
#               'isContinuous': <bool>,
#               'isAway': <bool>,  
#               'justArrived': <bool>
#               'justLeft': <bool>,  
#               'hasChanged': <bool>
#           },
#           {
#               'isMainUser': <bool>
#               'name': <string>,
#               'firstSeen': <int>,
#               'updatedSeen': <int>,
#               'lastSeen': <int>,
#               'isContinuous': <bool>,
#               'isAway': <bool>,  
#               'justArrived': <bool>
#               'justLeft': <bool>,  
#               'hasChanged': <bool>
#           }, 
#           ...
#       ]
#   }