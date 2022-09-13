"""
This module provides the logic for inserting new rows into the database
and retrieving metrics from database.
"""
import logging
from mysql.connector import connect, Error

class DatabaseConnection:
    """
    Object containing the information and logic required to
    insert rows into the database and retrieve the necessary data
    to build metrics.
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def execute(self, query):
        """
        Execute the given SQL query on the database.
        """
        result = ""
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
            ) as connection:
                with connection.cursor() as cursor:
                    result = cursor.execute(query)
                    connection.commit()

        except Error as error:
            logging.critical(error)

        return result

    def insert_row(self, result):
        """
        This method will insert a new row into the "state" table with the given result.
        """
        query = f"INSERT INTO state (healthy) VALUES ({result});"
        self.execute(query)

    def print_table(self):
        """
        Print everything in the "state" table.
        """
        print(self.execute("select * from state;"))

    def get_uptime(self):
        """
        Calculate the most recent uptime of the API.
        """
        return "Uptime is not yet calculated"

    def get_downtime(self):
        """
        Calculate the most recent downtime of the API.
        """
        return "Downtime is not yet calculated"

    def get_average_uptime(self):
        """
        Calculate the average uptime of the API over the past 7 days.
        """
        return "Average uptime is not yet calculated"
