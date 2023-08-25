# Importing required modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

# Function to send emails
def send_email(subject, msg, recipients, email, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = email
        message.attach(MIMEText(msg, "html"))
        text = message.as_string()

        for recipient in recipients:
            server.sendmail(email, recipient, text)

        server.quit()
        logging.info("Success: Email sent!")
    except Exception as e:
        logging.error(f"Email failed to send: {e}")
