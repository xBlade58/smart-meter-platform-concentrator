import os
import random
from paho.mqtt import client as mqtt_client
from mqtt_connection import MqttBrokerConnection

# Connection for subscription
iot_broker = os.environ['MQTT_BROKER_HOST']
iot_broker_port = int(os.environ['MQTT_BROKER_PORT'])
topic = "mytopic/test"
client_id = f'subscribe-{random.randint(0, 100)}'
iot_broker_conn = MqttBrokerConnection(iot_broker, iot_broker_port, 'iot-edge-sub')

# Connection for publishing to Cloud Broker
cloud_broker = os.environ['EMQX_CLOUD_HOST']
cloud_broker_port = int(os.environ['EMQX_CLOUD_PORT'])
cloud_broker_conn = MqttBrokerConnection(cloud_broker, cloud_broker_port, 'iot-edge-pub')


def subscribe(client_sub: mqtt_client.Client, client_pub: mqtt_client.Client):
    def on_message(client_sub, userdata, msg):
        result = client_pub.publish(msg.topic, msg.payload.decode())
        print(result)
        status = result[0]
        if status != 0:
            print(f'Failed to send message to cloud')

    client_sub.subscribe(topic)
    client_sub.on_message = on_message


def run():
    client_pub: mqtt_client.Client = cloud_broker_conn.client
    client_pub.loop_start()
    client_sub = iot_broker_conn.client
    subscribe(client_sub=client_sub, client_pub=client_pub)
    client_sub.loop_forever()
    print("END OF PROGRAM")
    client_pub.loop_stop() # or rather start() stop() ?


if __name__ == '__main__':
    run()
