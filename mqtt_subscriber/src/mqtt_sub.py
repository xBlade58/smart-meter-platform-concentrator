import json
import os
import random
from paho.mqtt import client as mqtt_client
from mqtt_connection import MqttBrokerConnection

# Connection for subscription
iot_broker = os.environ['MQTT_BROKER_HOST']
iot_broker_port = int(os.environ['MQTT_BROKER_PORT'])
topic_prod = 'SHRDZM/8CAAB550F854/8CAAB550F854/sensor'
client_id = f'subscribe-{random.randint(0, 100)}'
iot_broker_conn = MqttBrokerConnection(iot_broker, iot_broker_port, 'concentrator-sub', use_tls=False)

# Connection for publishing to Cloud Broker
meter_id = 'bf17c6a0-82ce-4214-adbd-5a7e4ecdb0ff'
concentrator_id = 'd38dbc62-57e0-4ea0-b10e-06ec0a538b1b'
cloud_broker = os.environ['EMQX_CLOUD_HOST']
cloud_broker_port = int(os.environ['EMQX_CLOUD_PORT'])
cloud_broker_conn = MqttBrokerConnection(cloud_broker, cloud_broker_port, 'concentrator-pub', use_tls=False)
topic=f'concentrator/{concentrator_id}/smartMeterMessage/{meter_id}/readings'


def subscribe(client_sub: mqtt_client.Client, client_pub: mqtt_client.Client):
    def on_message(client_sub, userdata, msg):
        msg = json.loads(msg.payload.decode())
        msg['meterId'] = meter_id
        json_msg = json.dumps(msg)
        print('Sedning final msg: \n', json_msg)
        result = client_pub.publish(topic, json_msg)
        status = result[0]
        if status != 0:
            print(f'Failed to send message to cloud')

    client_sub.subscribe(topic_prod)
    client_sub.on_message = on_message


def run():
    client_pub: mqtt_client.Client = cloud_broker_conn.client
    client_pub.loop_start()
    client_sub = iot_broker_conn.client
    subscribe(client_sub=client_sub, client_pub=client_pub)
    client_sub.loop_forever()
    print('END OF PROGRAM')
    client_pub.loop_stop() # or rather start() stop() ?


if __name__ == '__main__':
    run()
