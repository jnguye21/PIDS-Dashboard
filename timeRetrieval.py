from datetime import datetime, timedelta
import time
import dateutil.relativedelta

# variables ending with 'Time' are in YYYY-MM-DD HH:MM:SS
# variables ending with 'Epoch' are in Unix time
def getTimeDiff(employeeEpoch, currentTime):
    employeeTime = datetime.fromtimestamp(employeeEpoch) 
    diffEpoch = dateutil.relativedelta.relativedelta (currentTime, employeeTime)

    timeInfo = ""

    # same day only
    if diffEpoch.day is None:
        if diffEpoch.hours > 0:
            timeInfo += "{} hour".format(diffEpoch.hours)
            if diffEpoch.hours > 1:
                timeInfo += "s"
        if diffEpoch.minutes > 0:
            timeInfo += " {} minute".format(diffEpoch.minutes)
            if diffEpoch.minutes > 1:
                timeInfo += "s"
        if diffEpoch.seconds > 0:
            timeInfo += " {} second".format(diffEpoch.seconds)
            if diffEpoch.seconds > 1:
                timeInfo += "s"

    return timeInfo

# returns time only; only used in preliminary wifi testing
def timeConvWifi(lastSeen):
    lastSeen = lastSeen[-9:-1] # DOES NOT ACCOUNT FOR DAY
    hour = int(lastSeen[:2])
    hour -= 4
    lastSeen = str(hour) + lastSeen[2:]

    return lastSeen