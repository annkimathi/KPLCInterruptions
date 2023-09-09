# Importing required modules
from config import *
from email_service import send_email
from scraper_service import get_latest_interruption_pdf, download_pdf
from ocr_service import ocr_pdf, extract_date_time
import os
from datetime import datetime


def read_file(file_path):
    with open(f"templates/{file_path}", "r") as f:
        return f.read()

def main():
    file_path = None
    scheduled_html = read_file('scheduled_interruption.html')
    no_scheduled_html = read_file('no_scheduled_interruption.html')
    styles = read_file('email_styles.css')
    try:
        pdf_link = get_latest_interruption_pdf(URL_TO_SCRAPE)
        if pdf_link:
            logging.info(f"Downloading PDF: {pdf_link}")
            file_path = download_pdf(pdf_link)
            text = ocr_pdf(file_path)
            if len(text) < 50:
                logging.error("OCR output is suspiciously short. Please verify the content of the PDF.")

        today = datetime.now()

        for i in range(len(recipients)):
            date, time = extract_date_time(text, locations[i])
            if date and time:
                try:
                    scheduled_date = datetime.strptime(date, "%A %d.%m.%Y")
                except ValueError as e:
                    logging.error(f"Failed to parse the date: {e}")
                    continue

                if scheduled_date.date() < today.date():
                    logging.info("The scheduled interruption date has already passed. No email will be sent.")
                    continue

                subject = f"Scheduled Power Interruption for '{locations[i]}'"
                msg = scheduled_html.format(location=locations[i].upper(), date=date, time=time, styles=styles)

            else:
                subject = f"No Scheduled Maintenance for '{locations[i]}'"
                msg = no_scheduled_html.format(location=locations[i].upper(), styles=styles)

            send_email(subject, msg, [recipients[i]], email, password, file_path)

    finally:
        if file_path:
            os.remove(file_path)


# Main entry point of the script
if __name__ == "__main__":
    main()