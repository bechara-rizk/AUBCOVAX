from django.test import TestCase
import scheduling
import datetime
# Create your tests here.

today=datetime.datetime.today().strftime('%Y-%m-%d')
today=datetime.date(int(today[:4]),int(today[5:7]),int(today[8:10]))
print(today)

# for i in range(2):
#     Appt,time=scheduling.getFirstAppointment(today)
#     print(Appt,time)

print(scheduling.viewAvailableAppointmentsRange(today,2))