#implement scheduling using class with a dictionary and functions inside

import json
import datetime
import time


# dict: keys are the available days, values are lists, each elemenet in a list is a list of 2 elements: [start time, taken or free]
#str(datetime.date(2023,4,19)) is 2023-4-19
# to convert str back to datetime.date: datetime.datetime.strptime("2023-4-19", "%Y-%m-%d").date()

schd=dict()
times=["8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]
indexes={"8:00":0,"8:30":1,"9:00":2,"9:30":3,"10:00":4,"10:30":5,"11:00":6,"11:30":7,"12:00":8,"12:30":9,"13:00":10,"13:30":11,"14:00":12,"14:30":13,"15:00":14,"15:30":15,"16:00":16,"16:30":17,"17:00":18,"17:30":19}
timesAndAvailability=[[times[i],True] for i in range(len(times))]

# date=str(datetime.date(2023,4,19))
# if date not in schd:
#     schd[date]=timesAndAvailability.copy()
# date=str(datetime.date(2023,4,20))
# if date not in schd:
#     schd[date]=timesAndAvailability.copy()

# outputJson=json.dumps(schd, indent=4)
# file=open("mysite/main/schedule.json","w")
# file.write(outputJson)
# file.close()


file=open("mysite/main/schedule.json","r")
schd=json.load(file)
file.close()
print(schd['2023-04-19'])