from vjmail import EmailSender

# Configure the email sender with your SMTP server details
email_sender = EmailSender(
    smtp_server='imap.gmail.com',
    username='vjbots2023@gmail.com',
    password='ohwk unsh xpwb zjvy',
    smtp_port=587
)

# Send an email
email_sender.send_email(
    from_addr='vjbots2023@gmail.com',
    subject='Test Email 2',
    body='This is a test email sent using EmailSender library.'
)