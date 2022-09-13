import argparse
import logging
import requests
import sys
import time

from EmailService import email_service
from DatabaseConnection import DatabaseConnection

logging.getLogger().setLevel(logging.INFO)


class ApiMonitor:
    def __init__(self, url, db, support_email="testymctester653@gmail.com", sleep_time=5):
        self.url = url
        self.recipient = support_email
        self.fail_subject = f"URGENT: API ({self.url}) is down!"
        self.recovery_subject = f"API ({self.url}) has recovered from an outage!"
        self.sleep_time=sleep_time
        self.email_service = email_service
        self.db = db

    def get(self):
        try:
            response = requests.get(self.url)
        except Exception as e:
            logging.critical(e, exc_info=True)
            return False

        if response.status_code != 200:
            logging.error("Failed to invoke API.")
            return False

        else:
            logging.info("API is up.")

        json = response.json()
        
        try:
            status = json['status']
        except KeyError:
            return False
        
        if status != "OK":
            return False
        
        return True

    def start_monitoring(self):
        last_state = True # initialize, assuming API is up
        consecutive_changes = 0
        self.monitor = True

        try:
            while self.monitor:
                try:
                    status = self.get()
                except:
                    status = False

                if status != last_state:
                    consecutive_changes += 1

                if consecutive_changes >= 2:
                    last_state = status
                    if status:
                        self.db.insert_row(True)
                        self.send_email(self.email_service, self.recipient, self.recovery_subject, self.build_recovery_body())
                        logging.info("API recovered from outage.")
                    else:
                        self.db.insert_row(True)
                        self.send_email(self.email_service, self.recipient, self.fail_subject, self.build_outage_body())
                    consecutive_changes = 0

                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            logging.info("Bye")
            sys.exit()

    def send_email(self, e_service, recipient, subject, body_text):
        e_service(recipient, subject, body_text)

    def build_outage_body(self):
        uptime = self.db.get_uptime()
        avg_up = self.db.get_average_uptime()
        return f"""
        This is an URGENT email. The API @ {self.url} is DOWN!
        Prior to this outage, the API was up for {uptime}.
        Average uptime for API over the past 7 days: {avg_up}
        """

    def build_recovery_body(self):
        downtime = self.db.get_downtime()
        avg_up = self.db.get_average_uptime()
        return f"""
        The API @ {self.url} has recovered from an outage!
        Prior to this recovery, the API was down for {downtime}.
        Average uptime for API over the past 7 days: {avg_up}
        """


if __name__ == "__main__":
    url = "https://api.qa.fitpay.ninja/health"

    parser = argparse.ArgumentParser()
    parser.add_argument("--support", help = "The email address to send to.", required=True)
    parser.add_argument("--db_host", help = "The host of the mysql database.", required=True)
    parser.add_argument("--db_user", help = "The username for the mysql db.", required=True)
    parser.add_argument("--db_pw", help = "The password of the mysql db.", required=True)
    args = parser.parse_args()

    db = DatabaseConnection(args.db_host, args.db_user, args.db_pw, )
    monitor = ApiMonitor(url, db, args.support)
    monitor.start_monitoring()