from Synergy.StudentVue import StudentVue
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

sv = StudentVue('<INSERT_STUDENT_ID>','<INSERT_STUDENT_PASS>','28AEFB35-49E5-4BA0-9257-77352DD1F4E5')
classes = sv.get_classes()
grades = sv.get_grades()
missing_assignments = sv.get_missing_assignments()
output = []
for x in range(len(classes)):
    output.append("Grade in " + classes[x] + ": " + grades[x])
    if int(missing_assignments[x][0]) > 0:
        output.append("You have " + missing_assignments[x] + " in " + classes[x])
me = "<INSERT_SENDER_EMAIL>"
you = "<INSERT_PERSONAL_EMAIL>"
msg = MIMEMultipart('alternative')
msg['Subject'] = "Your StudentVue Grade Report " + str(datetime.datetime.now().date())
msg['From'] = me
msg['To'] = you
text = "\n".join(output)
part1 = MIMEText(text, 'plain')
msg.attach(part1)
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login('<INSERT_SENDER_EMAIL_USER>', '<INSERT_SENDER_EMAIL_PASS>')
mail.sendmail(me, you, msg.as_string())
mail.quit()