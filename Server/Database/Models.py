import datetime
import time
import os

from pymongo import MongoClient
import paho.mqtt.client as paho
from paho import mqtt

# MongoDB connection URI
uri = "mongodb+srv://antgroup0905:0905168232@cluster0.jph72eg.mongodb.net/test?retryWrites=true&w=majority"

# MQTT broker configuration 8883
broker_address = "broker.hivemq.com"
client_mqtt = paho.Client()
client_mqtt.connect(broker_address)
mqtt_topic = "newtesting"

# MQTT broker configuration 1883
"""
broker_address = "bed165964f054c00883721e64b049610.s1.eu.hivemq.cloud"
client_mqtt = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client_mqtt.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client_mqtt.username_pw_set(username="Hieu_esp32", password="Emvaytrang123")
client_mqtt.connect(broker_address, port=8883)
mqtt_topic = "Tezt" 
"""

# Connect to MongoDB
client = MongoClient(uri)
db = client.sensor
data_sensor = db.data_sensor

# Initialize temperature and humidity
temperature = 0
humidity = 0


# Callback function when receiving data from MQTT broker
def on_message(client_mqtt, userdata, message):
    global temperature, humidity
    # Get data from message payload
    data = message.payload.decode()
    temperature, humidity = map(float, data.split(","))


# Set the callback function for MQTT client
client_mqtt.on_message = on_message
client_mqtt.subscribe(mqtt_topic)

client_mqtt.loop_start()

# Loop every 10 seconds
while True:
    try:
        # Get the current timestamp
        timestamp = datetime.datetime.now()

        # Create a new document to insert into MongoDB
        data = {
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
        }

        # Insert data into MongoDB
        result = data_sensor.insert_one(data)
        document_id = result.inserted_id
        print("Inserted document with id: {}".format(document_id))

        # Print temperature and humidity information
        print("Temperature:", temperature)
        print("Humidity:", humidity)

        # Wait for 10 seconds
        time.sleep(10)

    except KeyboardInterrupt:
        # Stop MQTT client when receiving Ctrl+C keyboard interrupt
        client_mqtt.loop_stop()
        break
