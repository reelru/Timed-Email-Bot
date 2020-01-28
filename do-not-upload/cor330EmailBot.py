import smtplib
import ssl
import datetime
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

password = "ZPibZz4m99%E^1hbaE7Yn&5mD6clKO&x"
sender = "corereminderbot@gmail.com"
emails = ['jonathan.bara@mymail.champlain.edu', 'amaya.baustert@mymail.champlain.edu', \
'ari.blechman@mymail.champlain.edu', 'charlotte.bull@mymail.champlain.edu', \
'nurit.elber@mymail.champlain.edu', 'ian.eubanks@mymail.champlain.edu', \
'teagan.finnegan@mymail.champlain.edu', 'andrew.gorham@mymail.champlain.edu', \
'josh.henderson@mymail.champlain.edu', 'stephen.hill@mymail.champlain.edu', \
'richard.honiker@mymail.champlain.edu', 'ari.kaye@mymail.champlain.edu', \
'liam.kelly@mymail.champlain.edu', 'cameron.kimball@mymail.champlain.edu', \
'alex.labella@mymail.champlain.edu', 'jessie.lago@mymail.champlain.edu', \
'miranda.mallery@mymail.champlain.edu', 'stephen.neuger@mymail.champlain.edu', \
'alexis.piro@mymail.champlain.edu', 'cecilia.pohlar@mymail.champlain.edu', \
'ella.rackers@mymail.champlain.edu', 'kevin.rode@mymail.champlain.edu', \
'jacob.rodjenski@mymail.champlain.edu', 'colin.seiler@mymail.champlain.edu', \
'rodney.wheeler@mymail.champlain.edu']

emails = ["ella00rose@gmail.com"]

subjectBase = "COR330-10 Auto Discussion Reminder"
bodyBase = "This is an automatic reminder that your COR330-10 (Finding Japan: A Cinematic Journey) discussion is due"
bodyBase2 = "<a href=\"https://champlain.instructure.com/courses/1267179/discussion_topics\">Click Here</a> to be redirected to your course."
signature = "--------------------------------<br>     Beep Boop, I\'m a Bot<br>  Responses aren\'t monitored<br>--------------------------------"
sendDays = [1,4]
dueDate = 2
# Will not send emails
# Prints out message data
debug = True

# init basic vars
port = 465
context = ssl.create_default_context()

message = MIMEMultipart("alternative")
message["From"] = sender
message["To"] = sender
message["CC"] = ",".join(emails)

currentTime = datetime.datetime.now()
sentToday = False

while(True):
    currentTime = datetime.datetime.now()
    print("Checking the weekday...")
    # Check if the email has already been sent once today
    # Check if it's after noon
    # Check if it's a sending day
    # Weekdays mon=0 tues=1 wed=2 thurs=3 fri=4 sat=5 sun=6
    print("Today is", currentTime.weekday(), "and we send on.", sendDays)
    print("We have ", "not " if not sentToday else "","sent an email today.", sep="")
    print("The time is ", currentTime.hour, ":", currentTime.minute, sep="")
    print("It is ", "not " if currentTime.hour < 12 else "", "after noon.", sep="")
    if (currentTime.weekday() in sendDays) and not sentToday and currentTime.hour >= 12:
        print("Compiling email...")

        # Get current date information
        currentTime = datetime.datetime.now()

        # Check which coming day is the next dueDate
        for day in range(1,8):
            test = datetime.date.today() + datetime.timedelta(days=day)
            if test.weekday() == dueDate:
                nextDueDate = test

        # Add the due date to the subject line
        message["Subject"] = "[DUE: " + str(nextDueDate.month) + "/" + str(nextDueDate.day) + "] "+ subjectBase

        # Create the email body with the due date
        htmlStart = "<span style=\"font-family:monospace\">"
        htmlEnd = "</span>"
        body = "<html><body><div>" + htmlStart + bodyBase + " in " + str((nextDueDate-currentTime.date()).days) + " days on " + str(nextDueDate.month) + "/" + str(nextDueDate.day) + ".<br>" + bodyBase2 + "<br>" + signature + htmlEnd + "</div></body></html>"
        body = re.sub("<br>", htmlEnd + "<br>" + htmlStart, body)
        htmlBody = MIMEText(body, "html")
        message.attach(htmlBody)

        print("Sending email...")
        try:
            if debug:
                print("\nBody:\n")
                print(body)
                print("\nWhole Message:\n")
                print(message)
            else:
                # Connect and log into the server
                server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
                server.login(sender, password)
                # Send the email and save any errors
                errors = server.sendmail(sender, emails, message.as_string())
                server.close()

            # If there were any errors, print them out
            errors = {}
            if len(errors) > 0:

                print("Partial success.")
                errInfo = ""
                bigUser = -1
                for key, (id, error) in errors.items():
                    if len(key) > bigUser:
                        bigUser = len(key)
                    errInfo += key + "\t"
                    errInfo += str(id) + "  \t" + str(error)[2:len(str(error))-1]
                print("Email",end='')
                for tab in range(1,int((bigUser-(bigUser%4))/4)):
                    print("\t",end='')
                print("ID", "Error", sep="  \t")
                print(errInfo)

            # Otherwise, just print success
            else:
                print("Email successfully sent.")
            # Set this to true so no more emails are sent.
            sentToday = True

        # If it doesn't work at all
        except Exception as exp:

            # Close connection just in case
            server.close()
            # Print info
            print("Something went wrong sending the email. Will try again.")
            print("Exception: ", exp)

    # Wait for an hour if it's not noon yet
    elif not sentToday and (currentTime.weekday() in sendDays):

        print("Going to sleep for an hour...")
        time.sleep(3600)

    # If this isn't a sending day, reset sentToday to false so it will email
    # on the next designated day.
    elif not (currentTime.weekday() in sendDays):

        print("Today is not a designated day.")
        sentToday = False

    # If the message has been sent and it's still the designated day or
    # if it's not a sending day, wait until tomorrow.
    if (sentToday and currentTime.weekday() in sendDays) or (currentTime.weekday() not in sendDays):

        hours = 23 - currentTime.hour
        minutes = 60 - currentTime.minute
        print("Going to sleep until tomorrow (",end='')
        print(hours, "hours and", minutes, "minutes)...")
        secondsTotal = hours*3600 + minutes*60
        time.sleep(secondsTotal)

    # If nothing else matches, sleep for 15 seconds to avoid running this
    # loop over and over super fast
    else:
        time.sleep(15)
