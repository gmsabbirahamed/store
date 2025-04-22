import paho.mqtt.client as mqtt

# MQTT broker details
BROKER = "broker2.com"
PORT = 1883
USERNAME = "admin"
PASSWORD = "admin"

# Topics
SUB_TOPIC = "a/sub"
PUB_TOPIC = "a/pub"

# Callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(SUB_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

# Callback function for receiving messages
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Initialize MQTT client
client = mqtt.Client()

# Set username and password
client.username_pw_set(USERNAME, PASSWORD)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
client.connect(BROKER, PORT, keepalive=60)

# Function to publish a message
def publish_message(message):
    client.publish(PUB_TOPIC, message)
    print(f"Published message: {message} to topic {PUB_TOPIC}")

# Start the loop in a background thread
client.loop_start()

try:
    while True:
        # Publish a test message or get input
        message = input("Enter message to publish (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        publish_message(message)
except KeyboardInterrupt:
    print("Exiting...")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()
