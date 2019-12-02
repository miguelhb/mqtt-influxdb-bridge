#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge
This script receives MQTT data and saves those to InfluxDB.
"""

import requests
from requests.exceptions import HTTPError

import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'gisai'
INFLUXDB_PASSWORD = 'gisai'
INFLUXDB_DATABASE = 'gisai'

MQTT_ADDRESS = '10.30.1.250'
#MQTT_USER = 'mqttuser'
#MQTT_PASSWORD = 'mqttpassword'
MQTT_TOPIC = 'casa/#'  # [bme280|mijia]/[temperature|humidity|battery|status]
MQTT_REGEX = 'casa/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
        test(sensor_data)


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(location, measurement, float(payload))
    else:
        return None


def _send_sensor_data_to_influxdb(sensor_data):
    print('Guardando datos')
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    print(json_body)
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def test(sensor_data):
    # data to be sent to api 
    data = {"$class": "org.example.sensornetwork.NewMeasure", 
            "room": "Room1",#"sensor_data.location", 
            "supervisor": "SV1", 
            "temp": 5,#sensor_data.measurement, 
            "hum": 0, 
            "timestamp": "2019-12-02T14:09:23.108Z"} 
    for url in ['http://localhost:3000/api/NewMeasure']:#'https://api.github.com', 'https://api.github.com/invalid']:
        try:
            #response = requests.get(url)
            response = requests.post(url, data = data) 

            # If the response was successful, no Exception will be raised
            respo = response.text
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            print(respo)
            
def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
 #   mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()
   

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
main()
