# python3.6

import random

from paho.mqtt import client as mqtt_client
import json

broker = '192.168.1.3'
# broker = 'demo.thingsboard.io'
port = 1883
topic1 = "/test_mqtt_kiet_giang/qos1"
topic2 = "/test_mqtt_kiet_giang/qos0"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN1 = "u4DtGkP6ouo3Sl11zrTe"
ACCESS_TOKEN2 = "fp0MgrHmFjubV21mkec0"
# MQTT topics
TELEMETRY_TOPIC = "v1/devices/me/telemetry"

# Callback when the client connects to the MQTT broker
def on_connect1(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Callback when a message is published
def on_publish1(client, userdata, mid):
    print("Message Published")

# Create an MQTT client instance
client1 = mqtt_client.Client()
client2 = mqtt_client.Client()
# Set callback functions
client1.on_connect = on_connect1
client1.on_publish = on_publish1

client2.on_connect = on_connect1
client2.on_publish = on_publish1

# Connect to the ThingsBoard MQTT broker
client1.username_pw_set(ACCESS_TOKEN1)
client1.connect(THINGSBOARD_HOST, 1883, 60)

client2.username_pw_set(ACCESS_TOKEN2)
client2.connect(THINGSBOARD_HOST, 1883, 60)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# telemetry_data = {"temperature": 25}

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == topic1:
            telemetry_data = {"temperature": msg.payload.decode()}
            # client1.publish(TELEMETRY_TOPIC, payload=msg.payload.decode(), qos=1)
            client1.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)

            print("Published Telemetry: {}".format(telemetry_data))
        elif msg.topic == topic2:
            telemetry_data = {"temperature": msg.payload.decode()}
            # client1.publish(TELEMETRY_TOPIC, payload=msg.payload.decode(), qos=1)
            client2.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)

            print("Published Telemetry: {}".format(telemetry_data))
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = on_message


def run():
    a = 1
    client = connect_mqtt()
    subscribe(client)
    # client.loop_forever()
    client.loop_start()
    client1.loop_start()
    while (a == 1) :
        a = 1
if __name__ == '__main__':
    run()

# import asyncio
# import paho.mqtt.client as mqtt
# # from aiocoap import Context, Message

# # MQTT settings
# mqtt_broker_address = "mqtt.eclipse.org"
# mqtt_topic1 = "your/mqtt/topic1"
# mqtt_topic2 = "your/mqtt/topic2"

# # CoAP settings
# coap_server_address = "coap://localhost:5683"
# coap_path = "/your/coap/resource"

# # MQTT callback functions
# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT broker with result code "+str(rc))
#     client.subscribe(mqtt_topic1)
#     client.subscribe(mqtt_topic2)

# def on_message(client, userdata, msg):
#     print("Received MQTT message on topic {}: {}".format(msg.topic, msg.payload.decode()))

#     # Check the topic and perform actions accordingly
#     if msg.topic == mqtt_topic1:
#         # Do something for topic1
#         print("Handling message for topic1")
#     elif msg.topic == mqtt_topic2:
#         # Do something for topic2
#         print("Handling message for topic2")

# # CoAP callback function
# # async def coap_request():
# #     context = await Context.create_client_context()
# #     request = Message(code=2, uri=coap_server_address + coap_path, mtype=Message.CON)
# #     response = await context.request(request).response
# #     print("Received CoAP response: {}".format(response.payload.decode()))

# # Set up MQTT client
# mqtt_client = mqtt.Client()
# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message

# # Connect to MQTT broker
# mqtt_client.connect(mqtt_broker_address, 1883, 60)

# # Start the MQTT loop in a separate thread
# mqtt_client.loop_start()

# # Make a CoAP request
# # asyncio.run(coap_request())

# # Wait for a while to allow receiving MQTT messages
# mqtt_client.loop_stop()
# mqtt_client.disconnect()
