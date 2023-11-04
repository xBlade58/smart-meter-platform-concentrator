FROM python:3.12-slim
WORKDIR /subscriber/
COPY requirements.txt .
COPY src/mqtt_sub.py src/
COPY src/mqtt_connection.py src/
RUN pip3 install -r requirements.txt
CMD [ "python3", "src/mqtt_sub.py"]
