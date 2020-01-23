import smtplib
import ssl
import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

password = "password"
sender = "example@gmail.com"
emails = ["example@gmail.com", "example@gmail.com"]
subjectBase = "Example"
bodyBase = "Example Body"
signature = "From,<br>Example"
sendDays = [2,4]
dueDate = 2

# init basic vars
port = 465
context = ssl.create_default_context()

message = MIMEMultipart("alternative")
message["From"] = sender
message["To"] = ",".join(emails)

currentTime = datetime.datetime.now()
sentToday = False

while(True):
    print("Checking the weekday...")
    # Check if the email has already been sent once today
    # Check if it's after noon
    # Check if it's a sending day
    # Weekdays mon=0 tues=1 wed=2 thurs=3 fri=4 sat=5 sun=6
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
        body = "<html><body><div>" + bodyBase + "<br>Your assignment is due in " + str((nextDueDate-currentTime.date()).days) + " days on " + str(nextDueDate.month) + "/" + str(nextDueDate.day) + ".<br>" + signature + "</div></body></html>"
        htmlBody = MIMEText(body, "html")
        message.attach(htmlBody)

        print("Sending email...")
        try:
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
