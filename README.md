# AUBCOVAX

Tested on python 3.10.9
Need to install: pip install django django-crispy-forms crispy_bootstrap5

## Introduction:
The AUBCOVAX is a mobile application that manages the vaccination process of a specific population/country. The application should provide first the medical team with an interface to confirm vaccination dose one and two, and second the patients with an interface to register for the vaccine and view their certificate after successfully getting the second dose.
Since a large number of people are using the same application and hence sharing the same scheduling database, then the application should be able to communicate with a centralized database that holds all patient records, user records, centralized scheduled records, and certificate record.

## Workflow:
A. A patient can access the main registration page and enter his or her information:
• Full Name
• Date of birth
• ID card number
• Phone number
• Email
• City and Country
• Any medical conditions
• Credentials (username and password)
Afterwards, the patient can save his or her information, which will be sent directly to the centralized server over the network (not stored on the mobile phone).
After that an Email or SMS is sent to patient assigning him the first available time slot. Consider each time slot to be 30 minutes, and vaccination is given 10 hours per day, from 8:00 am till 6:00 pm.

B. A Medical personnel can access the application (assume already registered in the database / added manually) using his or her credentials, and search for a patient by
phone number. The vaccination history of the patient should appear, and the user
(medical person) can check the vaccination status of this specific patient.

C. If the patient’s dose 1 was confirmed, the medical person can set an appointment for dose 2 on the first available time slot and inform the patient via SMS or email, whereas
if dose 2 was taken, a certificate is emailed to the patient.

D. The patient should be able to login and view his records at any time, but cannot update them.

E. All data (patient records, schedule, login, etc.) should be only stored at the server, and
fetched from the server or uploaded to the server when necessary.

F. An Admin can access the application and be able to view a list of medical personnel or
patients with relevant data.

## Functionality Requirements 
### Login Page:
• Login as patient
• Login as medical personnel
• Login as Admin
### Registration Page:
• Register as patient Dose confirmation Page:
• View patient dose history (limited information)
• Accessed only by medical personnel
• Enable search by phone number
### Patient information Page:
• Accessed by patients
• Can view personal information
• Can view dose information including confirmed doses and scheduled ones
• Can view and download certificate is available
### Admin Page:
• View all medical personnel (Full name and ID)
• Search for a patient by name of phone number and view his info discussed above.
### Additional Notes:
• You can use any programming language to create the server.
• You can use the database of your choice.
• If you end up using an android emulator, then the emulator and server should be on different machines and communicate over a network.
• Extra points are given for implementing the application on an android phone. 

## Deliverables:
• Project Demo and Presentation.
• Project Documentation/report including how to run the program.
• Server source code.
• Mobile application source code.
