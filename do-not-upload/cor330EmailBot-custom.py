import smtplib
import ssl
import datetime
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

#<span style="font-family:monospace">
#</span>

port = 465
password = "ZPibZz4m99%E^1hbaE7Yn&5mD6clKO&x"
context = ssl.create_default_context()
sender = "corereminderbot@gmail.com"

plainBody = """\
This is a test of the bot for COR330-10.
Please reply to this email so Ella knows you received it."""

body = "<span style=\"font-family:monospace\">" + re.sub(r"(\n|\r)","</span><br><span style=\"font-family:monospace\">", plainBody) + "</span>"

message = MIMEMultipart("alternative")
message["From"] = sender
message["To"] = "ella.rackers@mymail.champlain.edu"
message["CC"] = ",".join(emails)
message["Subject"] = "This is a test of a bot"
htmlBody = MIMEText(body, "html")
message.attach(htmlBody)

emails.append("ella.rackers@mymail.champlain.edu")

server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login("corereminderbot@gmail.com", password)
errors = server.sendmail(sender, emails, message.as_string())
server.close()
