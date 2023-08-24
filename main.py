import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pdf2image import convert_from_path
import pytesseract
import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging

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
    pdf_link = get_latest_interruption_pdf()
    if pdf_link:
        logging.info(f"Downloading PDF: {pdf_link}")
        file_path = download_pdf(pdf_link)
        text = ocr_pdf(file_path)

        if len(text) < 50:
            logging.error("OCR output is suspiciously short. Please verify the content of the PDF.")

        date, time = extract_date_time(text, DEFAULT_LOCATION)
        if date and time:
            subject = f"Scheduled Power Interruption for '{DEFAULT_LOCATION}'"
            msg = f"""
                <!DOCTYPE html>
                <html lang='en'>
                <body>
                <p>Greetings,</p>
                <p>This is to inform you that there is a Scheduled Power Interruption around the area: <b>{DEFAULT_LOCATION.upper()}</b> on the date: <b>{date}</b>.</p> 
                <p>The interruption will begin from <b>{time}</b>.</p>
                <p>Kindly make the necessary preparations to mitigate any inconveniences this may cause.</p>
                <br>
                <p>Thank you for your understanding on this matter.</p>
                <p>Best Regards,<br>Kenya Power and Lighting Company</p>
                </body>
                </html>
            """
            send_email(subject, msg, recipients)
        else:
            subject = f"No Scheduled Maintenance for '{DEFAULT_LOCATION}'"
            msg = f"""
                <!DOCTYPE html>
                <html lang='en'>
                <body>
                <p>Greetings,</p>
                <p>There is no planned power interruption for the area: <b>{DEFAULT_LOCATION.upper()}</b> in the next two weeks.</p>
                <p>If '{DEFAULT_LOCATION.upper()}' is critical for you or if you need more information, please contact our customer service for further details.</p>
                <br>
                <p>Thank you for your attention to this matter.</p>
                <p>Best Regards,<br>Kenya Power and Lighting Company</p>
                </body>
                </html>
            """
            send_email(subject, msg, recipients)

        os.remove(file_path)


if __name__ == "__main__":
    main()
