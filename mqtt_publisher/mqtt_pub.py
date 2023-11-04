import os
import click
import random
import time
import ijson
from paho.mqtt import client as mqtt_client

broker = os.environ['MQTT_BROKER_HOST']
port = int(os.environ['MQTT_BROKER_PORT'])
topic = "mytopic/test"
client_id = f'python-mqtt-{random.randint(0,1000)}'

""" loads entire file to memory
def read_sample_data(filename:str) -> list():
    f = open(filename, 'r')
    json_messages = json.load(f)
    print(f"size: {len(json_messages)}")
    return json_messages
"""

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print('Failed to connect, return cde %d\n', rc)
        
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    print(f"broker is {broker}, port is {port}")
    client.connect(broker, port)
    return client

def publish(client, input_file:str, interval:int, limit:int):

    # json objects read as streams instead of loading everything at once
    with open(input_file, 'r') as file:
        msg_count = 0
        for msg in ijson.items(file, 'item'):
            time.sleep(interval)
            print("Sending...")
            print(f"type of msg is: {type(msg)}")
            result = client.publish(topic, str(msg))
            status = result[0]
            if status != 0:
                print(f'Failed to send message to topic {topic}')
            msg_count += 1
            print(f"Nr. of sent messages: {msg_count}")
            if msg_count > limit:
                return

@click.command()
@click.option('--input-file', default='sample-data.json', help='Input JSON file')
@click.option('--interval', default=3, help='Interval in seconds in which data is sent')
@click.option('--limit', default=100, help='position until which sample data is read and sent')
def run(input_file, interval, limit):
    client = connect_mqtt()
    client.loop_start()
    publish(client, input_file, interval, limit)
    client.loop_stop()


if __name__ == '__main__':
    print("Running Publisher!")
    run()
            
