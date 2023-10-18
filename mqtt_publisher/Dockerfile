FROM python:3.12-slim
WORKDIR /publisher/
COPY requirements.txt .
COPY mqtt_pub.py .
COPY sample-data.json .
RUN pip3 install -r requirements.txt
CMD [ "python3", "mqtt_pub.py", "--limit", "500" ]
