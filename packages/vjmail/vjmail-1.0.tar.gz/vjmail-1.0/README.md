# VJMail

A simple library to centralize VJBots e-mails sendings to the controller.

## Installation

```bash
pip install vjmail
```

## Usage
Here is an example of how to use the `EmailSender` class:

```python
from vjmail import EmailSender

# Configure the email sender with your SMTP server details
email_sender = EmailSender(
    smtp_server='smtp.example.com',
    username='your_email@example.com',
    password='your_password',
    smtp_port=587  # Optional, can be omitted if not required
)

# Send an email
email_sender.send_email(
    from_addr='your_email@example.com',
    subject='Test Email',
    body='This is a test email sent using EmailSender library.'
)
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.