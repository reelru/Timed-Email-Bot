This script was created on Python 3.8. Other 3.X versions may or may not work.

Dependancies:
	smtplib
	ssl
	datetime
	time
	from email.mime.text, MIMEText
	from email.mime.multipart, MIMEMultipart
	
To use for your own purposes, change the following variables:

variable name		purpose
password		your originating email address's password in cleartext
sender			username of the originating email address in the format of a string.
			ex: "example@gmail.com"
emails			list of one or more email addresses to send to.
			ex: ["example@gmail.com", "example@gmail.com"]
subjectBase		a string with a subject line
			ex: "Example"
bodyBase		a string with the body of the message (formatted in html)
			ex: "Example Body"
signature		a string that will be put at the end of the body (formatted in html)
			not required for functionality.
			ex: "From,<br>Example"
sendDays		a list of integers that represent a day of the week where monday = 0
			ex: [0, 2, 3] (Monday, Wednesday, Thursday)
			this is when the email is actually sent out.
dueDate			an integer representing a day of the week where monday = 0
			this is the weekday of the repeating date of why you're notifying people.

Below is an example of what a simplified outgoing email might look like with the example variable values.

From: example@gmail.com
To: example@gmail.com,example@gmail.com
Subject: [DUE: 1/29] Example

Example Body
Your assignment is due in 5 days on 1/29.
From,
Example
