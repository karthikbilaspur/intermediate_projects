import imaplib
import email

def authenticate_email(email, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email, password)
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    mail.close()
    mail.logout()
    return True