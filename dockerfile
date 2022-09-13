FROM python:latest

COPY ApiMonitor.py ./
COPY DatabaseConnection.py ./
COPY EmailService.py ./
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
CMD [ "python", "./ApiMonitor.py", "--support",    \
      "testymctester653@gmail.com", "--db_host",   \
      "$DB_HOST", "--db_user", "$DB_USER", "--db_pw", \
      "$DB_PW"]