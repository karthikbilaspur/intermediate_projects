Overview
This project automates email sending using SMTP. It features dynamic email templates, attachment support and robust error handling.
Features
Dynamic Email Templates: Use Jinja2 templating engine for customized email content.
Attachment Support: Attach files to automated emails.
Error Handling: Robust error handling for SMTP exceptions.
Custom SMTP Server: Support for custom SMTP servers.
Security: Secure password storage and TLS/SSL encryption.
Requirements
Python 3.8+
smtplib, email and ssl libraries (built-in)
Jinja2 templating engine
SMTP server credentials
Installation
Clone repository: git clone https://github.com/your-username/email-automation.git
Install dependencies: pip install -r requirements.txt
Configure SMTP settings in config/smtp_config.py
Usage
Update email template in templates/email_template.html.
Add attachments to attachments/ directory.
Run automation script: python email_automation.py
Testing
Run unit tests: python -m unittest discover -s tests
Contributing
Fork repository.
Create feature branch.
Submit pull request.
License
MIT License
Author
