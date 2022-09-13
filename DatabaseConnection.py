import logging
from mysql.connector import connect, Error

class DatabaseConnection:
    def __init__(self, host, user, pw):
        self.host = host
        self.user = user
        self.pw = pw

    def create_db(self):
        create_db_query = "CREATE DATABASE garmin_api_monitor;"
        create_table_query = """
        CREATE TABLE state(
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            healthy BOOL
        );
        """
        print(self.execute(create_db_query))
        print(self.execute(create_table_query))        

    def execute(self, query):
        result = ""
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.pw,
            ) as connection:
                with connection.cursor() as cursor:
                    result = cursor.execute(query)
                    connection.commit()

        except Error as e:
            logging.critical(e)
        
        return result

    def insert_row(self, result):
        query = f"INSERT INTO state (healthy) VALUES ({result});"
        self.execute(query)

    def print_table(self):
        print(self.execute("select * from state;"))

    def get_uptime(self):
        return "Uptime is not yet calculated"

    def get_downtime(self):
        return "Downtime is not yet calculated"

    def get_average_uptime(self):
        return "Average uptime is not yet calculated"
