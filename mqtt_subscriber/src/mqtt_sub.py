import datetime
import json
import os
import random
import sys
import time
from paho.mqtt import client as mqtt_client
from mqtt_connection import MqttBrokerConnection

standard_utc_offset = time.timezone // 3600

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
        final_msg = adapt(msg)
        json_msg = json.dumps(final_msg)
        print('Sedning final msg: \n', json_msg)
        result = client_pub.publish(topic, json_msg)
        status = result[0]
        if status != 0:
            print(f'Failed to send message to cloud')
        sys.stdout.flush()

    
    def adapt(msg):
        property_values = [
            {
                "propertyName": "1.7.0",
                "numericalValue": msg["1.7.0"],
                "unit": "kW"
            },
            {
                "propertyName": "1.8.0",
                "numericalValue": msg["1.8.0"],
                "unit": "kWh"
            },
            {
                "propertyName": "2.7.0",
                "numericalValue": msg["2.7.0"],
                "unit": "kWh"
            },
            {
                "propertyName": "2.8.0",
                "numericalValue": msg["2.8.0"],
                "unit": "kWh"
            },
            {
                "propertyName": "3.8.0",
                "numericalValue": msg["3.8.0"],
                "unit": "kWh"                
            },
            {
                "propertyName": "4.8.0",
                "numericalValue": msg["4.8.0"],
                "unit": "kvarh"
            },
            {
                "propertyName": "16.7.0",
                "numericalValue": msg["16.7.0"],
                "unit": "kW"
            },         
            {
                "propertyName": "31.7.0",
                "numericalValue": msg["31.7.0"],
                "unit": "A"
            },
            {
                "propertyName": "32.7.0",
                "numericalValue": msg["32.7.0"],
                "unit": "V"
            },
            {
                "propertyName": "51.7.0",
                "numericalValue": msg["51.7.0"],
                "unit": "A"
            },
            {
                "propertyName": "52.7.0",
                "numericalValue": msg["52.7.0"],
                "unit": "V"
            },
            {
                "propertyName": "71.7.0",
                "numericalValue": msg["71.7.0"],
                "unit": "A"
            },
            {
                "propertyName": "72.7.0",
                "numericalValue": msg["72.7.0"],
                "unit": "V"
            }
        ]

        final_readingTime = f"{msg['timestamp']}{get_system_timezone_offset()}"
        print(final_readingTime)
        final_msg = {
            "readingTime": final_readingTime,
            "meterId": meter_id,
            "propertyValues": property_values
        }
        return final_msg


    def get_system_timezone_offset():
        local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

        # Get the UTC offset
        offset_seconds = local_timezone.utcoffset(datetime.datetime.now()).total_seconds()

        # Convert the offset to the format (e.g. "+01:00")
        offset_hours = int(offset_seconds // 3600)
        offset_minutes = int((offset_seconds % 3600) // 60)
        offset_sign = '+' if offset_hours >= 0 else '-'

        # Format the offset
        offset_str = f"{offset_sign}{abs(offset_hours):02d}:{abs(offset_minutes):02d}"

        return offset_str


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
