import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def notify(message):
    sender = 'your-email@gmail.com'
    receiver = 'recipient-email@gmail.com'
    password = 'your-email-password'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Backup Notification'

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()