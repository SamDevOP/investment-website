from datetime import datetime,timedelta
import time

to_day=datetime.now() 

print("Today is : ",to_day)

new_date=datetime.today() + timedelta(days=2)

print(new_date)



for x in range(0,6):
    countdown=int((new_date-datetime.now()).total_seconds())

#print(countdown)
    days = countdown//86400
    hours = (countdown-days*86400)//3600
    minutes = (countdown-days*86400-hours*3600)//60
    seconds = countdown-days*86400-hours*3600-minutes*60
    print("{} days {} hours {} minutes {} seconds left".format(days, hours, minutes, seconds))
    time.sleep(5)