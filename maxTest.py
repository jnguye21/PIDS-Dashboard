deviceHistory = {
       'deviceList': [
           {
               'isMainUser': False,
               'name': 'b',
               'updatedSeen': 1,
               'justLeft': False
           },
           {
               'isMainUser': True,
               'name': 'a',
               'updatedSeen': 2,
               'justLeft': False
           },
          {
               'isMainUser': False,
               'name': 'c',
               'updatedSeen': 3,
               'justLeft': False
           }
       ]
}

#print(max(deviceHistory['deviceList']['updatedSeen']))
seq = [x['updatedSeen'] for x in deviceHistory['deviceList']]
maxTime = max(seq)
print(maxTime)
