# Importing required modules
import os
import logging
from dotenv import load_dotenv

# Configuration and Setup
load_dotenv()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

URL_TO_SCRAPE = "https://kplc.co.ke/category/view/50/planned-power-interruptions"

email = os.getenv('MAIL_USERNAME')
password = os.getenv('MAIL_PASSWORD')
recipients_locations = os.getenv('RECIPIENTS_LOCATIONS').split(',')

# Split the recipient email and their location
recipients = [r.split(':')[0] for r in recipients_locations]
locations = [r.split(':')[1] for r in recipients_locations]

if not email or not password or not recipients or not locations:
    logging.error("One or more environment variables are missing!")
    exit(1)
