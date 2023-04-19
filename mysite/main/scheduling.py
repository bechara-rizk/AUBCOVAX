#implement scheduling using class with a dictionary and functions inside

import json
import datetime


# dict: keys are the available days, values are lists, each elemenet in a list is a list of 2 elements: [start time, taken or free]
#str(datetime.date(2023,4,19)) is 2023-4-19
# to convert str back to datetime.date: datetime.datetime.strptime("2023-4-19", "%Y-%m-%d").date()

schd=dict()
times=["8:00","8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]
indexes={"8:00":0,"8:30":1,"9:00":2,"9:30":3,"10:00":4,"10:30":5,"11:00":6,"11:30":7,"12:00":8,"12:30":9,"13:00":10,"13:30":11,"14:00":12,"14:30":13,"15:00":14,"15:30":15,"16:00":16,"16:30":17,"17:00":18,"17:30":19}
reverse={0:"8:00",1:"8:30",2:"9:00",3:"9:30",4:"10:00",5:"10:30",6:"11:00",7:"11:30",8:"12:00",9:"12:30",10:"13:00",11:"13:30",12:"14:00",13:"14:30",14:"15:00",15:"15:30",16:"16:00",17:"16:30",18:"17:00",19:"17:30"}
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


# file=open("mysite/main/schedule.json","r")
# schd=json.load(file)
# file.close()
# print(schd['2023-04-19'])

def openSchd() -> dict:
    file=open("mysite/main/schedule.json","r")
    try:
        schd=json.load(file)
    except:
        schd=dict()
    file.close()
    return schd

def saveSchd(schd:dict):
    outputJson=json.dumps(schd, indent=4)
    file=open("mysite/main/schedule.json","w")
    file.write(outputJson)
    file.close()

def bookAppointment(date:datetime.date, time:str) -> bool:
    schd=openSchd()
    date=str(date)
    if date not in schd:
        schd[date]=timesAndAvailability.copy()
    if schd[date][indexes[time]][1]:
        schd[date][indexes[time]][1]=False
        saveSchd(schd)
        return True
    else:
        return False
    
def getFirstAppointment(today:datetime.date) -> "datetime.datetime, str":
    schd=openSchd()
    date=today+datetime.timedelta(days=1)#give appointments starting from tomorrow
    date=str(date)
    if date not in schd:
        #in this case all appointments are available
        schd[date]=timesAndAvailability.copy()
        schd[date][0][1]=False
        Appointment=datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
        time=reverse[0]
    else:
        #need to get first available timeslot
        times=schd[date]
        condition=True
        while(condition):
            for i in range(len(times)):
                if times[i][1]:
                    times[i][1]=False
                    Appointment=datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
                    time=reverse[i]
                    condition=False
                    break
            if condition:
                date=str(datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))+datetime.timedelta(days=1))
                if date not in schd:
                    schd[date]=timesAndAvailability.copy()
                    schd[date][0][1]=False
                    Appointment=datetime.date(int(date[:4]),int(date[5:7]),int(date[8:10]))
                    time=reverse[0]
                    condition=False
                else:
                    times=schd[date]
    saveSchd(schd)
    return Appointment,time

def viewAvailableAppointmentsRange(start:datetime.date,rangeInt:int) -> list:
    schd=openSchd()
    times=[]
    for i in range(rangeInt):
        date=str(start+datetime.timedelta(days=i))
        if date not in schd:
            schd[date]=timesAndAvailability.copy()
            for j in schd[date]:
                if j[1]:
                    times.append(date+" "+j[0])
        else:
            for j in schd[date]:
                if j[1]:
                    times.append(date+" "+j[0])
    
    saveSchd(schd)
    return times