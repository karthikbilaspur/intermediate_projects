import smtplib
from email.mime.multipart import MIMEMultipart
import ssl

def send_email(smtp_server, smtp_port, from_addr, password, to_addrs, msg):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())