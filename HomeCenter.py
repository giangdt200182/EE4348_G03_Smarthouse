# python3.6

import random
import socket

from paho.mqtt import client as mqtt_client
import json
import logging
import asyncio
import random
from aiocoap import Context, Message, Code, error

broker = '192.168.213.214'
# broker = 'demo.thingsboard.io'
port = 1883
topic1 = "/test_mqtt_kiet_giang/qos1" #nhan du lieu truyen len tu cam bien temperature
topic2 = "/test_mqtt_kiet_giang/qos0" #nhan trang thai cua ccch temperature
topic3 = "/test_mqtt_kiet_giang/qos2" #truyen tin hieu dieu khien ve ccch cua temperature
uri1 = 'coap://192.168.213.32:5683/Data' #sensor
uri2 = 'coap://192.168.213.75:5683/Data' #led

observe_data = True
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN1 = "dmq6ojfnxbnkfywcpqf6"
ACCESS_TOKEN2 = "gelaOn5rUXBvpOKbEI0W"
ACCESS_TOKEN3 = "3ON1RbMJWG6htGCDihvi"
ACCESS_TOKEN4 = 'Gfon6w1rqOtKhUM5r9Gq'
ACCESS_TOKEN5 = 'vco5HuybZFIxbmeA9TiB'
ACCESS_TOKEN6 = "f8RCCK3TcPAduVin2abf"
# MQTT topics
TELEMETRY_TOPIC = "v1/devices/me/telemetry"
ATTRIBUTE_TOPIC = "v1/devices/me/attributes"
RPC_TOPIC = "v1/devices/me/rpc/request/+"

button_state = {"enabled": False}
def extract_adc_values(adc_response):
    # Sử dụng hàm split để tách chuỗi thành danh sách
    adc_values = adc_response.split(',')

    # Kiểm tra xem có đúng là hai giá trị hay không
    if len(adc_values) == 2:
        str1 = adc_values[0].strip()  # strip để loại bỏ khoảng trắng xung quanh
        str2 = adc_values[1].strip()
        return str1, str2
    else:
        # Trả về giá trị mặc định nếu không tìm thấy kết quả
        return None, None

def setValue (params):
    button_state['enabled'] = params
    print("Rx setValue is : ",button_state)

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        # Create a socket object
        socket.create_connection((host, port), timeout=timeout)
        print("Internet connection is available.")
        return True
    except OSError:
        print("No internet connection.")
        return False

# Callback when the client connects to the MQTT broker
def on_connect1(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Callback when a message is published
def on_publish1(client, userdata, mid):
    print("Message Published")

# Create an MQTT client instance
client1 = mqtt_client.Client()#truyen du lieu temperature tu HC len thingsboard
client2 = mqtt_client.Client()#truyen du lieu humidity tu HC len thingsboard
client3 = mqtt_client.Client()#truyen trang thai cua ccch temperature len thingsboard
client4 = mqtt_client.Client()#truyen trang thai cua ccch humidity len thingsboard
client5 = mqtt_client.Client()#nhan tin hieu dieu khien tu switch cua ccch cua temperature xuong hc
client6 = mqtt_client.Client()#nhan tin hieu dieu khien tu switch cua ccch cua humidity xuong hc
# Set callback functions
client1.on_connect = on_connect1
client1.on_publish = on_publish1

client2.on_connect = on_connect1
client2.on_publish = on_publish1

client3.on_connect = on_connect1
client3.on_publish = on_publish1

client4.on_connect = on_connect1
client4.on_publish = on_publish1


# Connect to the ThingsBoard MQTT broker
client1.username_pw_set(ACCESS_TOKEN1)
client1.connect(THINGSBOARD_HOST, 1883, 60)

client2.username_pw_set(ACCESS_TOKEN2)
client2.connect(THINGSBOARD_HOST, 1883, 60)

client3.username_pw_set(ACCESS_TOKEN3)
client3.connect(THINGSBOARD_HOST, 1883, 60)

client4.username_pw_set(ACCESS_TOKEN4)
client4.connect(THINGSBOARD_HOST, 1883, 60)

client5.username_pw_set(ACCESS_TOKEN5)
client5.connect(THINGSBOARD_HOST,1883,60)

client6.username_pw_set(ACCESS_TOKEN6)
client6.connect(THINGSBOARD_HOST,1883,60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
client0 = mqtt_client.Client(client_id) #nhan du lieu tu cac cam bien truyen len va gui tin hieu dieu khien xuong cac co cau chap hanh
# client.username_pw_set(username, password)
client0.on_connect = on_connect
client0.connect(broker, port)
def on_message(client, userdata, msg):
    # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    internet_connection = check_internet_connection()
    if msg.topic == topic1:
        str1,str2 = extract_adc_values(msg.payload.decode())
        if internet_connection:
            telemetry_data = {"temperature": str1,"humidity": str2}
            # client1.publish(TELEMETRY_TOPIC, payload=msg.payload.decode(), qos=1)
            client1.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            print("Published Telemetry: {}".format(telemetry_data))
        else:
            print("Lost internet Connection!!!!!!")
            print(str1)
            if int(str1)>20:
                gpio = 0
                client0.publish(topic3,gpio)
                # print("vao duoc if roi")
        
    elif msg.topic == topic2:
        if internet_connection:
            telemetry_data = {"status": msg.payload.decode()}
            # client1.publish(TELEMETRY_TOPIC, payload=msg.payload.decode(), qos=1)
            client3.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            client5.publish(ATTRIBUTE_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            print("Published Telemetry: {}".format(telemetry_data))
client0.subscribe(topic1)
client0.subscribe(topic2)
client0.on_message = on_message

def on_connect2(client, userdata, flags, rc):
    print("rc code:",rc)
    client.subscribe('v1/devices/me/rpc/request/+')
# MQTT on_message caallback function
def on_message2(client, userdata, msg):
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        print("requestId : ",requestId)
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            print("getvalue request\n")
            print("sent getValue : ",button_state)
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(button_state), 1)
        if data['method'] == 'setValue':
            print("setvalue request\n")
            params = data['params']
            setValue(params)
            print(params)
            client.publish('v1/devices/me/attributes', json.dumps(button_state), 1)
            # client0.publish(topic3,params)
            if params == True:
                gpio = 1
                client0.publish(topic3,gpio)
                print(1)
            else:
                gpio = 0
                client0.publish(topic3,gpio)
                print(0)

def on_connect3(client, userdata, flags, rc):
    print("rc code:",rc)
    client.subscribe('v1/devices/me/rpc/request/+')
# MQTT on_message caallback function
def on_message3(client, userdata, msg):
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        print("requestId : ",requestId)
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            print("getvalue request\n")
            print("sent getValue : ",button_state)
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(button_state), 1)
        if data['method'] == 'setValue':
            print("setvalue request\n")
            params = data['params']
            setValue(params)
            print(params)
            client.publish('v1/devices/me/attributes', json.dumps(button_state), 1)
            # client0.publish(topic3,params)
            if params == True:
                gpio = 1
            else:
                gpio = 0
            payload = gpio
            print(payload)
            asyncio.run(coap_post_request_client(payload))
            
client5.on_connect = on_connect2
client5.on_message = on_message2

# client5.username_pw_set(ACCESS_TOKEN5)
# client5.connect(THINGSBOARD_HOST,1883,60)

client6.on_connect = on_connect3
client6.on_message = on_message3

logging.basicConfig(level=logging.INFO)

# Function to observe the state of a CoAP resource on the server using a GET request
async def observe_coap_get_request_data(uri,client):
    # Create a CoAP client context
    protocol = await Context.create_client_context()
    observe_value = 0

    while True:
        try:
            # Create a GET request with observe information
            request = Message(code=Code.GET, uri=uri, observe=observe_value)
            pr = protocol.request(request)

            # Send the request and receive the response from the server
            r = await pr.response
            # Display the response content
            print("Response from {}: {}".format(uri, r.payload.decode()))
            str1, str2 = extract_adc_values(r.payload.decode())
            if check_internet_connection():
                telemetry_data = {"temperature": str1, "humidity": str2}
                client.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            else:
                if int(str1)>200:
                    payload = 1
                    try:
                        # Convert the integer payload to bytes
                        payload_bytes = str(payload).encode('utf-8')
                        # Create a POST request with the created payload
                        post_request = Message(code=Code.POST, payload=payload_bytes)
                        post_request.set_request_uri("coap://192.168.213.75:5683/Control")

                        # Create a CoAP client context
                        context = await Context.create_client_context()

                        # Send the request and receive the response from the server
                        post_response = await context.request(post_request).response

                        # Display the response content
                        print(f"POST Response from server: {post_response.payload.decode('utf-8')}")
                    except error.RequestTimedOut:
                    # Handle the case where the request times out (no connection)
                        print("Timeout while sending POST request, trying again...")

                    except Exception as e:
                        # Handle any errors that occur while sending the request
                        print(f"POST Error: {e}")
                        
        except error.RequestTimedOut:
            print("Timeout while requesting {}, trying again...".format(uri))
    # Increase the observe value to send a new observe request
        # observe_value += 1
        except Exception as e:
            # Handle any other exceptions that may occur
            print("Error: {}".format(e))
        # Wait for 3 seconds before sending the next request
        await asyncio.sleep(1)
        
async def observe_coap_get_request_status(uri,client1,client2):
    # Create a CoAP client context
    protocol = await Context.create_client_context()
    observe_value = 0

    while True:
        try:
            # Create a GET request with observe information
            request = Message(code=Code.GET, uri=uri, observe=observe_value)
            pr = protocol.request(request)

            # Send the request and receive the response from the server
            r = await pr.response
            # Display the response content
            print("Response from {}: {}".format(uri, r.payload.decode()))
            str1, str2 = extract_adc_values(r.payload.decode())
            telemetry_data = {"status": str1}
            client1.publish(TELEMETRY_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            client2.publish(ATTRIBUTE_TOPIC, payload=json.dumps(telemetry_data), qos=1)
            if str1 == '1':
                time = int(str2)
                print(time)
                if time >= 4:
                    payload = 0
                    print(payload)
                    try:
                        # Convert the integer payload to bytes
                        payload_bytes = str(payload).encode('utf-8')
                        # Create a POST request with the created payload
                        post_request = Message(code=Code.POST, payload=payload_bytes)
                        post_request.set_request_uri("coap://192.168.213.75:5683/Control")

                        # Create a CoAP client context
                        context = await Context.create_client_context()

                        # Send the request and receive the response from the server
                        post_response = await context.request(post_request).response

                        # Display the response content
                        print(f"POST Response from server: {post_response.payload.decode('utf-8')}")
                    
                    except error.RequestTimedOut:
                        # Handle the case where the request times out (no connection)
                        print("Timeout while sending POST request, trying again...")

                    except Exception as e:
                        # Handle any errors that occur while sending the request
                        print(f"POST Error: {e}")
                                
        except error.RequestTimedOut:
            print("Timeout while requesting {}, trying again...".format(uri))
        # Increase the observe value to send a new observe request
        # observe_value += 1
        except Exception as e:
            # Handle any other exceptions that may occur
            print("Error: {}".format(e))
        # Wait for 3 seconds before sending the next request
        await asyncio.sleep(1)

# Function to send random POST requests to control a CoAP resource
async def coap_post_request_client(payload):
    print("Payload value:", payload)
    # while True:
        # Create a random payload (0 or 1)
        # payload = str(random.choice([0, 1])).encode('utf-8') #nhan tin hieu dieu khien tu Thingsboard
    try:
        # Convert the integer payload to bytes
        payload_bytes = str(payload).encode('utf-8')
        # Create a POST request with the created payload
        post_request = Message(code=Code.POST, payload=payload_bytes)
        post_request.set_request_uri("coap://192.168.213.75:5683/Control")

        # Create a CoAP client context
        context = await Context.create_client_context()

        # Send the request and receive the response from the server
        post_response = await context.request(post_request).response

        # Display the response content
        print(f"POST Response from server: {post_response.payload.decode('utf-8')}")
    
    except error.RequestTimedOut:
        # Handle the case where the request times out (no connection)
        print("Timeout while sending POST request, trying again...")

    except Exception as e:
        # Handle any errors that occur while sending the request
        print(f"POST Error: {e}")

        # Wait for 10 seconds before sending the next POST request
        # await asyncio.sleep(3)
# Main function that initializes the tasks
# async def main_coap():
#     tasks = [
#         observe_coap_get_request_data(uri1,client2),
#         observe_coap_get_request_status(uri2,client4,client6),
#         # coap_post_request_client()
#     ]
#     # Wait for all tasks to complete
#     await asyncio.gather(*tasks)
    
#     global observe_data
#     observe_data = check_internet_connection()
#     print("Giang123321Huhutachmonroi")
loop = asyncio.get_event_loop()
# Function to check internet connection in a separate thread
def check_internet_connection_async():
    return loop.run_in_executor(None, check_internet_connection)

# Main function that initializes the tasks
async def main_coap():
    tasks = [
        observe_coap_get_request_data(uri1, client2),
        observe_coap_get_request_status(uri2, client4, client6),
        # coap_post_request_client()
    ]
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    global observe_data
    observe_data = await check_internet_connection_async()
    print("Giang123321Huhutachmonroi")
    
def run():
    # a = 1
    client0.loop_start()
    client1.loop_start()
    client2.loop_start()
    client3.loop_start()
    client4.loop_start()
    client5.loop_start()
    client6.loop_start()
    asyncio.run(main_coap())
    print("hello")
    # while (a == 1) :
    #     a = 1
if __name__ == '__main__':
    run()

