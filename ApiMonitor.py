import argparse
import logging
import requests
import sys
import time

from EmailService import email_service

logging.getLogger().setLevel(logging.INFO)


class ApiMonitor:
    def __init__(self, url, support_email="testymctester653@gmail.com", sleep_time=5):
        self.url = url
        self.recipient = support_email
        self.fail_message = f"URGENT: API ({self.url}) is down!"
        self.recovery_message = f"API ({self.url}) has recovered from an outage!"
        self.sleep_time=sleep_time
        self.email_service = email_service

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
                        self.send_email(self.email_service, self.recipient, self.recovery_message, self.recovery_message)
                        logging.info("API recovered from outage.")
                    else:
                        self.send_email(self.email_service, self.recipient, self.fail_message, self.fail_message)
                    consecutive_changes = 0

                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            logging.info("Bye")
            sys.exit()

    def send_email(self, e_service, recipient, subject, body_text):
        e_service(recipient, subject, body_text)


if __name__ == "__main__":
    url = "https://api.qa.fitpay.ninja/health"

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--support", help = "The email address to send to.", required=True)
    args = parser.parse_args()

    monitor = ApiMonitor(url, args.support)
    monitor.start_monitoring()