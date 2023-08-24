# Kenya Power Planned Power Interruption Notifier

## Description

This Python application is designed to automate the process of notifying users about planned KPLC (Kenya Power and Lighting Company) power interruptions. It scrapes information from a specified URL, processes PDF files, and sends out email notifications.

## Prerequisites

- Tesseract: This application uses Tesseract for OCR (Optical Character Recognition). Make sure to install it and add it to your system path. For installation guide, please refer to the [Tesseract Documentation](https://tesseract-ocr.github.io/tessdoc/).

## Features

- Web scraping to gather power interruption data
- PDF parsing for detailed information
- Email notifications to multiple recipients
- Logging for better traceability and debugging
- Environment variable support for configuration

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/annkimathi/KPLCInterruptions.git
    ```

2. Navigate into the project directory:

    ```bash
    cd KPLCInterruptions
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

The application uses the following environment variables:

- `MAIL_USERNAME`: Your email address
- `MAIL_PASSWORD`: Your email password
- `RECIPIENTS`: Comma-separated list of email recipients
- `LOCATION`: Default location for power interruption monitoring

Copy the `.env.example` to `.env` and fill in these variables.

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
