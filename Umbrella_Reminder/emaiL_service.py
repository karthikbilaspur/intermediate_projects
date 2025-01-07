import smtplib
from email.mime.text import MIMEText

def send_email(email, subject, body):
    email_password = "YOUR_EMAIL_PASSWORD"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, email_password)
    server.sendmail(email, email, msg.as_string())
    server.quit()