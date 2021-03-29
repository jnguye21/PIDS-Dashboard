import schedule, sys, time

from employeeParse import getInfo

# global list/dictionary
from globals import deviceHistory, NUMBER_EMPLOYEES

def main():    
    try:
        schedule.every(60).seconds.do(getInfo)
    
        while True:
            schedule.run_pending()
            time.sleep(1)    
    
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()