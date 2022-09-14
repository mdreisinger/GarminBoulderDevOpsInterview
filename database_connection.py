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
    def __init__(self, host, user, password, database_name):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name

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
                database=self.database_name
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(query)
                    connection.commit()
                    result = cursor.fetchall()

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
        for row in self.execute("select * from state;"):
            print(row)

    def get_uptime(self):
        """
        Calculate the most recent uptime of the API.
        """
        query = """
        SELECT timestamp, healthy,
        TIMEDIFF(timestamp, LAG(timestamp) OVER (ORDER BY id)) AS diff
        FROM state;
        """

        result = self.execute(query)
        return [entry[2] for entry in result if entry[1]==0].pop()


    def get_downtime(self):
        """
        Calculate the most recent downtime of the API.
        """
        query = """
        SELECT timestamp, healthy,
        TIMEDIFF(timestamp, LAG(timestamp) OVER (ORDER BY id)) AS diff
        FROM state;
        """

        result = self.execute(query)
        return [entry[2] for entry in result if entry[1]==1].pop()
        