import logging
import smtplib


def email_service(email, body):
    try:
        smtpObj = smtplib.SMTP('localhost', 1025)
        smtpObj.sendmail("mike.dreisinger95@gmail.com", email, body)         
        logging.info("Successfully sent email")
    except smtplib.SMTPException:
        logging.error("Error: unable to send email")