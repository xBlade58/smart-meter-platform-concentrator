FROM python:3.12-slim
ARG TZ=Europe/Vienna
ENV TZ=${TZ}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /subscriber/
COPY requirements.txt .
COPY src/ src/
COPY certs/ certs/
RUN pip3 install -r requirements.txt
CMD [ "python3", "src/mqtt_sub.py"]
