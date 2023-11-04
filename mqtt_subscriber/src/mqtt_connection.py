import os
from paho.mqtt import client as mqtt_client


class MqttBrokerConnection:

    def __init__(self, broker:str, port:int, client_id:str) -> None:
        self.__broker_host = broker
        self.__broker_port = port
        self.__client_id = client_id
        self.client: mqtt_client.Client = self.__connect_mqtt(self.__broker_host, self.__broker_port)


    def __connect_mqtt(self, broker:str, port:int) -> mqtt_client.Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print('Failed to connect, return cde %d\n', rc)
            
        client = mqtt_client.Client(self.__client_id)
        client.on_connect = on_connect
        print(f"broker is {broker}, port is {port}")
        client.connect(broker, port)
        return client
