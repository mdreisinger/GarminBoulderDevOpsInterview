"""
The main application file.
"""

import logging
import os
import sys
import time
import requests

from email_service import email_service
from database_connection import DatabaseConnection

logging.getLogger().setLevel(logging.INFO)


class ApiMonitor: # pylint: disable=too-many-instance-attributes
    """
    The main object which is capable of hitting the API and performing tasks based on the result.
    """
    def __init__(self, url, db_conn, support_email="testymctester653@gmail.com", sleep_time=5):
        self.url = url
        self.recipient = support_email
        self.fail_subject = f"URGENT: API ({self.url}) is down!"
        self.recovery_subject = f"API ({self.url}) has recovered from an outage!"
        self.sleep_time=sleep_time
        self.email_service = email_service
        self.db_conn = db_conn
        self.monitor = True

    def get(self):
        """
        Basic method that uses requests.get to hit the API.
        Returns False if status_code is not 200, or status is not OK.
        Returns True otherwise.
        """
        try:
            response = requests.get(self.url, timeout=10)
        except Exception as error: # pylint: disable=broad-except
            logging.critical(error, exc_info=True)
            return False

        if response.status_code != 200:
            logging.error("Failed to invoke API.")
            return False

        json = response.json()

        try:
            status = json['status']
        except KeyError:
            return False

        if status != "OK":
            return False

        logging.info("API is up.")

        return True

    def start_monitoring(self):
        """
        This is the main method used for this application. It repeatedly calls the get() method
        and sends emails, and updates the database when the health status of the API changes.
        """
        last_state = True # initialize, assuming API is up
        prev_loop_changed = False

        try:
            while self.monitor:
                status = self.get()
                if status != last_state and prev_loop_changed is True:
                    last_state = status
                    if status:
                        self.db_conn.insert_row(True)
                        self.send_email(self.email_service,
                                        self.recipient,
                                        self.recovery_subject,
                                        self.build_recovery_body())
                        logging.info("API recovered from outage.")
                    else:
                        self.db_conn.insert_row(False)
                        self.send_email(self.email_service,
                                        self.recipient,
                                        self.fail_subject,
                                        self.build_outage_body())

                elif status != last_state and prev_loop_changed is False:
                    prev_loop_changed = True

                if status == last_state:
                    prev_loop_changed = False

                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            logging.info("Bye")
            sys.exit()

    def send_email(self, e_service, recipient, subject, body_text):
        """
        This method uses the email service to send an email.
        It is written this way to accomodate unit testing.
        """
        e_service(recipient, subject, body_text)

    def build_outage_body(self):
        """
        This method returns a string which is intended to be used as the body
        of the email sent when an outage occurs.
        """
        uptime = self.db_conn.get_uptime()
        return f"""
        This is an URGENT email. The API @ {self.url} is DOWN!
        Prior to this outage, the API was up for {uptime}.
        """

    def build_recovery_body(self):
        """
        This method returns a string which is intended to be used as the body
        of the email sent when the API recovers from an outage.
        """
        downtime = self.db_conn.get_downtime()
        return f"""
        The API @ {self.url} has recovered from an outage!
        Prior to this recovery, the API was down for {downtime}.
        """


if __name__ == "__main__":
    api_url = os.getenv('API_URL')
    support = os.getenv('SUPPORT')
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_pw = os.getenv('DB_PW')
    db_name = os.getenv('DB_NAME')

    # pylint: disable=logging-fstring-interpolation
    logging.info(f"api_url: {api_url}")
    logging.info(f"support: {support}")
    logging.info(f"db_host: {db_host}")
    logging.info(f"db_user: {db_user}")
    logging.info(f"db_pw: {db_pw}") # what's security?
    logging.info(f"db_name: {db_name}")

    db = DatabaseConnection(db_host, db_user, db_pw, db_name)
    monitor = ApiMonitor(api_url, db, support)
    monitor.start_monitoring()
