#Logan Noel
#
#March 31 2017

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(toaddr,subject,message):
    fromaddr = "quickalert.py@gmail.com"
    base_message = '''
    \n\n\n
    ==================================================
    THIS NOTIFICATION HAS BEEN GENERATED AUTOMATICALLY
    ==================================================
    '''
    message = message + base_message
    msg = MIMEMultipart()
    msg['From'] = "quickalert.py@gmail.com"
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "mO9N3GYVT")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def wide_alert(subject, message):
    toaddrs = ['noel.logan2@gmail.com', 'justinni@usc.edu']
    for addr in toaddrs:
        send_mail(addr, subject, message)