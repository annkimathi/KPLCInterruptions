import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re


def get_latest_interruption_pdf(URL_TO_SCRAPE):
    try:
        response = requests.get(URL_TO_SCRAPE)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        current_year = datetime.now().strftime("%Y")
        current_month = datetime.now().strftime("%m")

        # A list to store dates and their corresponding URLs
        date_pdf_mapping = {}

        pdf_links = soup.find_all('a', href=True)
        for link in pdf_links:
            if ".pdf" in link['href'] and current_year in link['href']:
                # Extract date from the URL
                match = re.search(r'(\d{2}.\d{2}.\d{4})', link['href'])
                if match:
                    pdf_date_str = match.group(1)
                    pdf_date = datetime.strptime(pdf_date_str, "%d.%m.%Y")
                    date_pdf_mapping[pdf_date] = link['href']

        # Get the URL corresponding to the latest date
        latest_date = max(date_pdf_mapping.keys())
        return date_pdf_mapping[latest_date]

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
