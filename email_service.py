# Importing required modules
import smtplib
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Function to send emails
def send_email(subject, msg, recipients, email, password, file_path=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = email
        message.attach(MIMEText(msg, "html"))

        if file_path:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file_path, 'rb').read())
            encoders.encode_base64(part)
            # Extract the original filename from the file path
            original_filename = os.path.basename(file_path)
            part.add_header('Content-Disposition', f'attachment; filename="{original_filename}"')
            message.attach(part)

        text = message.as_string()

        for recipient in recipients:
            server.sendmail(email, recipient, text)

        server.quit()
        logging.info("Success: Emails sent!")
    except Exception as e:
        logging.error(f"Emails failed to send: {e}")
