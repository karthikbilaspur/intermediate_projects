import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl
import logging
from jinja2 import Environment, FileSystemLoader
from utils.email_utils import send_email
from utils.template_utils import render_template
from config.smtp_config import SMTPConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_automated_email(subject, template_name, data, from_addr, to_addrs, password, smtp_config):
    """
    Send automated email using SMTP.

    Args:
        subject (str): Email subject.
        template_name (str): Email template name.
        data (dict): Dynamic data for email template.
        from_addr (str): Sender's email address.
        to_addrs (list): List of recipient email addresses.
        password (str): Sender's email password.
        smtp_config (SMTPConfig): SMTP configuration.

    Returns:
        None
    """
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject

    # Render email template
    template_loader = Environment(loader=FileSystemLoader('templates'))
    html_body = render_template(template_loader, template_name, data)
    msg.attach(MIMEText(html_body, 'html'))

    # Add attachments
    attachments = ['attachment1.pdf', 'attachment2.docx']
    for attachment in attachments:
        with open(f'attachments/{attachment}', 'rb') as f:
            part = MIMEApplication(f.read(), Name=attachment)
            part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            msg.attach(part)

    try:
        send_email(smtp_config.server, smtp_config.port, from_addr, password, to_addrs, msg)
        logger.info(f"Email sent successfully to {', '.join(to_addrs)}")
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed.")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    subject = "Test Automated Email"
    template_name = "email_template.html"
    data = {'name': 'John Doe', 'email': 'johndoe@example.com'}
    from_addr = "your-email@gmail.com"
    to_addrs = ["recipient1-email@example.com", "recipient2-email@example.com"]
    password = "your-email-password"
    smtp_config = SMTPConfig('smtp.gmail.com', 587)

    send_automated_email(subject, template_name, data, from_addr, to_addrs, password, smtp_config)