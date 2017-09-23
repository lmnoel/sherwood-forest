#Logan Noel
#March 31 2017

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(fromaddr, toaddr, subject, message, pswd):
    '''
    Easily send a notification to yourself or as many
    people as you want.

        fromaddr: string (valid gmail address)
        pswd: string - login to fromaddr
        toaddr: list of strings (valid email addresses)
        subject: string
        message: string

    Returns True if message sent, else False.
    '''

    base_message = '''
    \n\n\n
    ==================================================
    THIS NOTIFICATION HAS BEEN GENERATED AUTOMATICALLY
    ==================================================
    '''
    message = message + base_message
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, pswd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return True
    except:
        return False
