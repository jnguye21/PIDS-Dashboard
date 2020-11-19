deviceHistory = {
       'deviceList': [
           {
               'isMainUser': False,
               'name': 'b',
               'justArrived': False,
               'justLeft': False
           },
           {
               'isMainUser': True,
               'name': 'a',
               'justArrived': False,
               'justLeft': False
           },
          {
               'isMainUser': False,
               'name': 'c',
               'justArrived': False,
               'justLeft': False
           }
       ]
}

deviceHistory['deviceList'] = sorted(deviceHistory['deviceList'], key = lambda i: 
    (i['isMainUser'], i['justArrived'], i['justLeft']), reverse = True)

for emp in deviceHistory['deviceList']: #[1:]:
    print(emp['name'])