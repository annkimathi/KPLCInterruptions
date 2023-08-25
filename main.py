import requests
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
import pytesseract
import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configuration and Setup
load_dotenv()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

URL_TO_SCRAPE = "https://kplc.co.ke/category/view/50/planned-power-interruptions"

email = os.getenv('MAIL_USERNAME')
password = os.getenv('MAIL_PASSWORD')
recipients = os.getenv('RECIPIENTS').split(',')

DEFAULT_LOCATION = os.getenv('LOCATION')

if not email or not password or not recipients or not DEFAULT_LOCATION:
    logging.error("One or more environment variables are missing!")
    exit(1)


def send_email(subject, msg, recipients):
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

        for recipient in recipients:  # Send email to every recipient separately
            server.sendmail(email, recipient, text)

        server.quit()
        logging.info("Success: Email sent!")
    except Exception as e:
        logging.error(f"Email failed to send: {e}")


def get_latest_interruption_pdf():
    try:
        response = requests.get(URL_TO_SCRAPE)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        current_year = datetime.now().strftime("%Y")
        current_month = datetime.now().strftime("%m")
        pdf_links = soup.find_all('a', href=True)
        for link in reversed(pdf_links):
            if ".pdf" in link['href'] and current_year in link['href'] and current_month in link['href']:
                return link['href']
        return None
    except Exception as e:
        logging.error(f"Error fetching PDF link: {e}")
        return None


def download_pdf(pdf_url, destination="temp.pdf"):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            file.write(response.content)
        return destination
    except Exception as e:
        logging.error(f"Error downloading PDF: {e}")
        return None


def ocr_pdf(file_path):
    try:
        # Convert PDF to list of images
        images = convert_from_path(file_path)
        # Perform OCR on each image and join the results
        text = ' '.join([pytesseract.image_to_string(image) for image in images])
        return text
    except Exception as e:
        logging.error(f"Error in OCR process: {e}")
        return None


def extract_date_time(text, location):
    sections = re.split(r'AREA:', text)[1:]
    for section in sections:
        if location in section and location not in section.split("DATE")[0]:
            match = re.search(r"DATE: (.*?) TIME: (.*?)\n", section)
            if match:
                date = match.group(1).strip()
                time = match.group(2).strip()
                return date, time
    return None, None


def main():
    file_path = None  # Initialize file_path variable
    try:
        pdf_link = get_latest_interruption_pdf()
        if pdf_link:
            logging.info(f"Downloading PDF: {pdf_link}")
            file_path = download_pdf(pdf_link)
            text = ocr_pdf(file_path)

            if len(text) < 50:
                logging.error("OCR output is suspiciously short. Please verify the content of the PDF.")

            date, time = extract_date_time(text, DEFAULT_LOCATION)
            if date and time:
                try:
                    scheduled_date = datetime.strptime(date, "%A %d.%m.%Y")
                except ValueError as e:
                    logging.error(f"Failed to parse the date: {e}")
                    return

                today = datetime.now()

                if scheduled_date.date() < today.date():
                    logging.info("The scheduled interruption date has already passed. No email will be sent.")
                    return

        if date and time:
            subject = f"Scheduled Power Interruption for '{DEFAULT_LOCATION}'"
            msg = f"""
                <!DOCTYPE html>
                <html lang='en'>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                        }}
                        .header {{
                            background-color: #f4f4f4;
                            padding: 10px;
                            text-align: center;
                        }}
                        .content {{
                            margin: 20px;
                            padding: 20px;
                            background-color: #fff;
                            border: 1px solid #ddd;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 10px;
                            background-color: #f4f4f4;
                        }}
                        .important-text {{
                            font-weight: bold;
                            color: red;
                        }}
                    </style>
                </head>
                <body>
                    <div class='header'>KPLC Notification</div>
                    <div class='content'>
                        <p>Greetings,</p>
                        <p>This is to inform you that there is a Scheduled Power Interruption around <span class='important-text'>{DEFAULT_LOCATION.upper()}</span> on <span class='important-text'>{date}</span></p>
                        <p>The interruption will begin from <span class='important-text'>{time}</span></p>
                        <p>Kindly make the necessary preparations to mitigate any inconveniences this may cause.</p>
                        <p>For more information, please contact:</p>
                        <p>National Contact Centre: 97771 or 0703 070 707 | 0732 170 170</p>
                        <p>USSD & Telephone Number: Dial *977# or +254 203201000</p>
                        <p>Email: <a href='mailto:customercare@kplc.co.ke'>customercare@kplc.co.ke</a></p>
                    </div>
                    <div class='footer'>Best Regards</div>
                </body>
                </html>
            """
            send_email(subject, msg, recipients)
        else:
            subject = f"No Scheduled Maintenance for '{DEFAULT_LOCATION}'"
            msg = f"""
                    <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                            }}
                            .header {{
                                background-color: #f4f4f4;
                                padding: 10px;
                                text-align: center;
                            }}
                            .content {{
                                margin: 20px;
                                padding: 20px;
                                background-color: #fff;
                                border: 1px solid #ddd;
                            }}
                            .footer {{
                                text-align: center;
                                padding: 10px;
                                background-color: #f4f4f4;
                            }}
                            .important-text {{
                                font-weight: bold;
                                color: red;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class='header'>KPLC Notification</div>
                        <div class='content'>
                            <p>Greetings,</p>
                            <p>Good news! There is no planned power interruption around <span class='important-text'>{DEFAULT_LOCATION.upper()}</span> in the next two weeks.</p>
                            <p>If you experience a power outage in your area or require additional information, please reach out to KPLC's customer service using the contact details provided below:</p>
                            <p>National Contact Centre: 97771 or 0703 070 707 | 0732 170 170</p>
                            <p>USSD & Telephone Number: Dial *977# or +254 203201000</p>
                            <p>Email: <a href='mailto:customercare@kplc.co.ke'>customercare@kplc.co.ke</a></p>
                        </div>
                        <div class='footer'>Best Regards</div>
                    </body>
                    </html>
                """
            send_email(subject, msg, recipients)

    finally:
        if file_path:
            os.remove(file_path)


if __name__ == "__main__":
    main()
