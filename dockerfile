FROM python:latest

COPY api_monitor.py ./
COPY database_connection.py ./
COPY email_service.py ./
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
CMD [ "python", "./ApiMonitor.py", "--support",    \
      "testymctester653@gmail.com", "--db_host",   \
      "$DB_HOST", "--db_user", "$DB_USER", "--db_pw", \
      "$DB_PW"]