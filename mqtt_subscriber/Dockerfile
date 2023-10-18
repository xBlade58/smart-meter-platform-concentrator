FROM python:3.12-slim
WORKDIR /subscriber/
COPY requirements.txt .
COPY mqtt_sub.py .
RUN pip3 install -r requirements.txt
CMD [ "python3", "mqtt_sub.py"]
