from pdf2image import convert_from_path
import pytesseract
import re
import logging

def ocr_pdf(file_path):
    try:
        images = convert_from_path(file_path)
        text = ' '.join([pytesseract.image_to_string(image) for image in images])
        return text
    except Exception as e:
        logging.error(f"Error in OCR process: {e}")
        return None

def extract_date_time(text, location):
    sections = re.split(r'AREA:', text)[1:]
    for section in sections:
        if location in section:
            match = re.search(r"DATE: (.*?) TIME: (.*?)\n", section)
            if match:
                date = match.group(1).strip()
                time = match.group(2).strip()
                return date, time
    return None, None
