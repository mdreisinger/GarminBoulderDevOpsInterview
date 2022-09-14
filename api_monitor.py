"""
The main application file.
"""

import argparse
import logging
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
        consecutive_changes = 0

        try:
            while self.monitor:
                status = self.get()
                if status != last_state:
                    consecutive_changes += 1

                if consecutive_changes >= 2:
                    last_state = status
                    if status:
                        self.db_conn.insert_row(True)
                        self.send_email(self.email_service,
                                        self.recipient,
                                        self.recovery_subject,
                                        self.build_recovery_body())
                        logging.info("API recovered from outage.")
                    else:
                        self.db_conn.insert_row(True)
                        self.send_email(self.email_service,
                                        self.recipient,
                                        self.fail_subject,
                                        self.build_outage_body())
                    consecutive_changes = 0

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
    API_URL = "https://api.qa.fitpay.ninja/health"

    parser = argparse.ArgumentParser()
    parser.add_argument("--support", help = "The email address to send to.", required=True)
    parser.add_argument("--db_host", help = "The host of the mysql database.", required=True)
    parser.add_argument("--db_user", help = "The username for the mysql db.", required=True)
    parser.add_argument("--db_pw", help = "The password of the mysql db.", required=True)
    parser.add_argument("--db_name", help = "The name of the mysql db.", required=True)
    args = parser.parse_args()

    db = DatabaseConnection(args.db_host, args.db_user, args.db_pw, args.db_name)
    monitor = ApiMonitor(API_URL, db, args.support)
    monitor.start_monitoring()