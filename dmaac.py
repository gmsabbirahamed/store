import paho.mqtt.client as mqtt

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully!")
        # Subscribe to the specified topic
        client.subscribe("DMA/AC/1209002409120000/CONTROL")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Set username and password for the broker
client.username_pw_set(username="broker2", password="Secret!@#$1234")  # Replace with your actual username

# Connect to the broker
broker_address = "broker2.dma-bd.com"
client.connect(broker_address, 1883, 60)

# Start the loop to process callbacks and handle reconnections
client.loop_forever()
