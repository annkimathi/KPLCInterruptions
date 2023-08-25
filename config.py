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
recipients = os.getenv('RECIPIENTS').split(',')
DEFAULT_LOCATION = os.getenv('LOCATION')

if not email or not password or not recipients or not DEFAULT_LOCATION:
    logging.error("One or more environment variables are missing!")
    exit(1)
