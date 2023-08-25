from config import *
from email_service import send_email
from scraper_service import get_latest_interruption_pdf, download_pdf
from ocr_service import ocr_pdf, extract_date_time
import os
from datetime import datetime

def main():
    file_path = None
    try:
        pdf_link = get_latest_interruption_pdf(URL_TO_SCRAPE)
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
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                        color: #333;
                        background-color: #f9f9f9;
                    }}
                    .header {{
                        background-color:#D22B2B;
                        padding: 20px;
                        text-align: center;
                        color: #fff;
                        font-size:24px;
                        border-radius:5px 5px 0 0;
                    }}
                    .content {{
                        margin: 20px;
                        padding: 20px;
                        background-color: #fff;
                        border: 1px solid #ddd;
                        border-radius:0 0 5px 5px;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 10px;
                        background-color: #f4f4f4;
                        border-top:1px solid #ddd;
                        color:#888;
                    }}
                    .important-text {{
                        font-weight: bold;
                        color: #D22B2B;
                    }}
                    p {{
                        line-height: 1.6;
                    }}
                </style>
            </head>
            <body>
                <div class='header'>Scheduled Power Interruption Notice</div>
                <div class='content'>
                    <p>Greetings,</p>
                    <p>We would like to inform you that there is a scheduled power interruption around <span class='important-text'>{DEFAULT_LOCATION.upper()}</span> on <span class='important-text'>{date}</span>.</p>
                    <p>The power interruption is expected to last from <span class='important-text'>{time}</span>.</p>
                    <p>Please adjust your plans accordingly to avoid any inconvenience. For more information, please contact:</p>
                    <p>KPLC National Contact Centre: <a href="tel:97771">97771</a> or <a href="tel:0703070707">0703 070 707</a> | <a href="tel:0732170170">0732 170 170</a></p>
                    <p>USSD & Telephone Number: Dial *977# or <a href="tel:+254203201000">+254 203201000</a></p>
                    <p>Email: <a href='mailto:customercare@kplc.co.ke'>customercare@kplc.co.ke</a></p>
                </div>
                <div class='footer'>
                  <p>Best Regards,</p>
                </div>
            </body>
            </html>
            """
            send_email(subject, msg, recipients, email, password)
        else:
            subject = f"No Scheduled Maintenance for '{DEFAULT_LOCATION}'"
            msg = f"""
            <!DOCTYPE html>
            <html lang='en'>
            <head>
                <style>
                    body {{
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                        color: #333;
                        background-color:#f9f9f9;
                    }}
                    .header {{
                        background-color:#28A745;
                        padding: 20px;
                        text-align: center;
                        color: #fff;
                        font-size:24px;
                        border-radius:5px 5px 0 0;
                    }}
                    .content {{
                        margin: 20px;
                        padding: 20px;
                        background-color: #fff;
                        border: 1px solid #ddd;
                        border-radius:0 0 5px 5px;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 10px;
                        background-color: #f4f4f4;
                        border-top:1px solid #ddd;
                        color:#888;
                    }}
                    .important-text {{
                        font-weight: bold;
                        color: #28A745;
                    }}
                    p {{
                        line-height: 1.6;
                    }}
                </style>
            </head>
            <body>
                <div class='header'>No Scheduled Power Interruption</div>
                <div class='content'>
                    <p>Greetings,</p>
                    <p>Good news! There is no planned power interruption around <span class='important-text'>{DEFAULT_LOCATION.upper()}</span> for the next two weeks.</p>
                    <p>If you experience a power outage in your area or require additional information, please reach out to KPLC's customer service using the contact details provided below:</p>
                    <p>KPLC National Contact Centre: <a href="tel:97771">97771</a> or <a href="tel:0703070707">0703 070 707</a> | <a href="tel:0732170170">0732 170 170</a></p>
                    <p>USSD & Telephone Number: Dial *977# or <a href="tel:+254203201000">+254 203201000</a></p>
                    <p>Email: <a href='mailto:customercare@kplc.co.ke'>customercare@kplc.co.ke</a></p>
                </div>
                <div class='footer'>
                  <p>Best Regards,</p>
                </div>
            </body>
            </html>
            """
            send_email(subject, msg, recipients, email, password)
    finally:
        if file_path:
            os.remove(file_path)


if __name__ == "__main__":
    main()
