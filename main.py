#from flask import Flask, json, request
import schedule, sys, time

from employeeParse import *

# global list/dictionary
from globals import deviceHistory, NUMBER_EMPLOYEES

def main():    
    try:
        schedule.every().minute.at(":30").do(getInfo)
    
        while True:
            schedule.run_pending()
            time.sleep(1)    
    
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()