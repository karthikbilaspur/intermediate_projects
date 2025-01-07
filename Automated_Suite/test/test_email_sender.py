import unittest
from email_sender import send_email
from unittest.mock import patch
from smtplib import SMTPException

class TestEmailSender(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        mock_smtp.return_value.sendmail.return_value = {}
        subject = "Test"
        message = "This is a test email"
        from_addr = "your-email@gmail.com"
        to_addr = "recipient-email@gmail.com"
        password = "your-email-password"
        send_email(subject, message, from_addr, to_addr, password)
        mock_smtp.return_value.sendmail.assert_called_once()

    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        mock_smtp.return_value.sendmail.side_effect = SMTPException
        subject = "Test"
        message = "This is a test email"
        from_addr = "your-email@gmail.com"
        to_addr = "recipient-email@gmail.com"
        password = "your-email-password"
        send_email(subject, message, from_addr, to_addr, password)
        mock_smtp.return_value.sendmail.assert_called_once()

    def test_send_email_invalid_recipient(self):
        subject = "Test"
        message = "This is a test email"
        from_addr = "your-email@gmail.com"
        to_addr = "invalid_recipient"
        password = "your-email-password"
        send_email(subject, message, from_addr, to_addr, password)

if __name__ == "__main__":
    unittest.main()