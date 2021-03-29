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
#               'isMainUser': <bool>        // if visually impaired user
#               'name': <string>,           // employee name
#               'firstSeen': <int>,         // initial time entered if currently in area
#               'updatedSeen': <int>,       // most recent time if currently in area
#               'lastSeen': <int>,          // last time present if no longer in area
#               'justArrived': <bool>       // just entered area
#               'isContinuous': <bool>,     // currently in area
#               'justLeft': <bool>,         // just left area
#               'isAway': <bool>,           // no longer in area
#               'hasChanged': <bool>        // either just entered or left area
#           },
#           ...
#       ]
#   }

