import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error

# MySQL connection settings
def create_connection():
    """Create and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # or your MySQL host
            user="root",
            password="12345678",
            database="mqtt_data"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Callback function when a message is received from the MQTT broker
def on_message(client, userdata, message):
    """Handle incoming MQTT messages and store them in MySQL."""
    try:
        msg_payload = message.payload.decode('utf-8')
        print(f"Received message: {msg_payload} on topic {message.topic}")
        
        # Store the received message in the MySQL database
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = "INSERT INTO sensor_data (topic, message) VALUES (%s, %s)"
                data = (message.topic, msg_payload)
                cursor.execute(insert_query, data)
                connection.commit()
                print("Data inserted into MySQL database")
            except Error as e:
                print(f"Error while inserting into MySQL: {e}")
            finally:
                if cursor:
                    cursor.close()
                connection.close()
    except Exception as e:
        print(f"Error handling MQTT message: {e}")

# MQTT settings
broker = "broker.hivemq.com"  # Public broker, replace if needed
port = 1883
topic = "sabbir/your/topic"  # Replace with your actual topic

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    """Callback when the client subscribes to a topic."""
    print(f"Subscribed to topic {topic} with QoS {granted_qos}")

def on_disconnect(client, userdata, rc):
    """Callback when the client disconnects from the broker."""
    print("Disconnected from MQTT broker")

# Create MQTT client instance using protocol version MQTTv311 to avoid deprecation warnings
client = mqtt.Client(protocol=mqtt.MQTTv311)

# Attach callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

# Connect to MQTT broker
client.connect(broker, port)

# Start the loop to process incoming MQTT messages
client.loop_forever()
