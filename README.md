# Kenya Power Planned Power Interruption Notifier

## Description

Python code designed to automate the process of notifying users about planned **KPLC** (**Kenya Power and Lighting Company**) power interruptions. It scrapes information from a specified URL, processes the latest PDF file, and sends out email notifications.

## Prerequisites

- **Tesseract**: This application uses Tesseract for OCR (Optical Character Recognition). Make sure to install it and add it to your system path. For installation guide, please refer to the [Tesseract Documentation](https://tesseract-ocr.github.io/tessdoc/).

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

## Automating the Script

To have the script run automatically at specified intervals, you can use Task Scheduler on Windows or Cron jobs on Linux/MacOS.

### Task Scheduler (Windows)

1. Open `Task Scheduler` by searching for it in the Start menu.
2. In the right-hand menu, click on `Create Basic Task...`.
3. Enter a name for your task and click `Next`.
4. Choose when you want the task to start (e.g., Daily, Weekly, etc.) and click `Next`.
5. Set the day and time you want the task to run, then click `Next`.
6. On the next screen, select `Start a program` and click `Next`.
7. Browse to the location of your Python executable (`python.exe`) in the `Program/script` field.
8. In the `Add arguments (optional)` field, type the script name (`main.py`).
9. In the `Start in (optional)` field, type the full path to your script's folder.
10. Click `Next` and then `Finish`.

### Cron Jobs (Linux/MacOS)

1. Open your terminal.

2. Type `crontab -e` to open the cron table for editing.

3. Add a new line to schedule your task, adhering to the cron time-and-date syntax:

    ```bash
    0 5 * * 6 /usr/bin/python3 /full/path/to/main.py
    ```
   
    - Replace `/usr/bin/python3` with the output of `which python3`.
    - Replace `/full/path/to/main.py` with the full path to your `main.py` script.

4. In this example, the cron job will run every Saturday at 5 a.m. GMT. Here's a breakdown of the fields in the cron schedule:

    - `0`: Minute field, set to 0.
    - `5`: Hour field, set to 5 (5 a.m.).
    - `*`: Day-of-month field, set to run every day of the month.
    - `*`: Month field, set to run every month.
    - `6`: Day-of-week field, set to 6, which represents Saturday (Sunday is 0, Monday is 1, ..., Saturday is 6).

   Note: The cron job runs based on the server's local time. If your server is set to GMT, the job should run at 5 a.m. GMT. If the server is set to a different time zone, you'll need to adjust the time accordingly.

5. Save the file and exit the editor to activate the cron job.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
