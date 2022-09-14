FROM python:latest

COPY api_monitor.py ./
COPY database_connection.py ./
COPY email_service.py ./
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

CMD [ "python", "./api_monitor.py"]