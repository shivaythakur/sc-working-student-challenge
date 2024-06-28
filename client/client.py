from threading import Event, Thread
from typing import Optional, Any
import queue
import requests
import json
import time

import paho.mqtt.client as mqtt

# Feel free to add more libraries (e.g.: The REST Client library)

mqtt_client: Optional[mqtt.Client] = None

mqtt_connection_event = Event()
wait_event = Event()
mqtt_topic="secret/number"
message_queue = queue.Queue()
Post_request_url="http://server:80/secret_number"
Secret_check_url="http://server:80/secret_correct"
server_ready_url="http://server:80/ready"
secret = -1


def send_secret_rest(secret_value: int):
    # Add the logic to send this secret value to the REST server.
    # We want to send a JSON structure to the endpoint `/secret_number`, using
    # a POST method.
    #
    # Assuming secret_value = 50, then the request will contain the following
    # body: {"value": 50}
    data = {"value": secret_value}
    try:
        response = requests.post(Post_request_url, json=data)
        if response.status_code == 200:
            print(f"Successfully posted the secret number {secret_value} to the REST server")

            # to check data integrity (secret sent and received)
            response=requests.get(Secret_check_url)
            if response.text == "YES":
                print("Secret received from server and sent by client are same")
            else:
                print("Secret received from server and sent by client are not same, mismatch between secret read and write")

        else:
            print(f"Failed to post to the REST server. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending POST request: {e}")
    


def on_mqtt_connect(client, userdata, flags, rc):
    if(rc==0):
        print('Connected to MQTT broker')
        mqtt_connection_event.set()
        client.subscribe(mqtt_topic)
    else:
        print("Failed to connect, return code %d\n", rc)

    #added condition in above method to fail the program in case it is failed to connect to mqtt broker
    


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    # Implement the logic to parse the received secret (we receive a json, but
    # we are interested just on the value) and send this value to the REST
    # server... or maybe the sending to REST should be done somewhere else...
    # do you have any idea why?

    try:
        payload = json.loads(msg.payload.decode())
        secret_number = payload.get("value")
        if secret_number is not None:
            print(f"Received secret number: {secret_number} from topic: {msg.topic}")

            # Put the secret number into the queue
            message_queue.put(secret_number)
            wait_event.wait(1)
            
    except json.JSONDecodeError:
        print("Failed to decode JSON from message payload")



def connect_mqtt() -> mqtt.Client:
    client = mqtt.Client(
        clean_session=True,
        protocol=mqtt.MQTTv311
    )
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    client.loop_start()
    client.connect('mqtt-broker', 1883)
    return client


def wait_for_server_ready():
    # Implement code to wait until the server is ready, it's up to you how
    # to do that. Our advice: Check the server source code and check if there
    # is anything useful that can help.
    # Hint: If you prefer, feel free to delete this method, use an external
    # tool and incorporate it in the Dockerfile

    #checking for a specified period of time if server is ready or not
    pass

    
    


def process_queue():
    while True:
        # Get the secret number from the queue
        secret_number = message_queue.get()
        if secret_number is None:
            break
        # Send the secret number to the REST server
        send_secret_rest(secret_number)



def main():
    global mqtt_client

    wait_for_server_ready()

    mqtt_client = connect_mqtt()
    mqtt_connection_event.wait()

    # At this point, we have our MQTT connection established, now we need to:
    # 1. Subscribe to the MQTT topic: secret/number
    # 2. Parse the received message and extract the secret number
    # 3. Send this number via REST to the server, using a POST method on the
    # resource `/secret_number`, with a JSON body like: {"value": 50}
    # 4. (Extra) Check the REST resource `/secret_correct` to ensure it was
    # properly set

    # Start the queue processing in a separate thread
    queue_thread = Thread(target=process_queue)
    queue_thread.start()

  # Keep the script running to process messages
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()

        # Signal the queue processing thread to exit
        message_queue.put(None)

        # Wait for the queue processing thread to finish
        queue_thread.join()


if __name__ == '__main__':
    main()
