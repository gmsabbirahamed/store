import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import datetime

# MySQL database connection setup
def create_connection():
    """Create and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",   # Replace with your MySQL host
            user="root",        # Replace with your MySQL user
            password="", # Replace with your MySQL password
            database="mqtt_data"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Callback function to handle received MQTT messages
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')
    print(f"Received '{payload}' from topic '{topic}'")

    # Prepare data for database insertion
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        data_1 = None
        data_2 = None

        # Check which topic the message is from and prepare the SQL query accordingly
        if topic == "sabbir/data1":
            data_1 = float(payload)
        elif topic == "sabbir/data2":
            data_2 = float(payload)


        # Insert or update the database depending on the data received
        try:
            if data:
                insert_query = """
                    INSERT INTO mqtt_data (data_1, data_2)
                    VALUES (%s, %s)
                """
                data = (data-1, data-2)
                cursor.execute(insert_query, data)
                connection.commit()
                print(f"Data inserted into MySQL for {data}")
            else:
                print("No data data available")
        except Error as e:
            print(f"Error inserting into MySQL: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database")

# MQTT settings
broker = "test.mosquitto.org"  # Public MQTT broker
port = 1883

# MQTT topics to subscribe to
topics = [
    "sabbir/data1",
    "sabbir/data2"
]

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        for topic in topics:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")
    
# Create an MQTT client
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port)

# Start the MQTT loop to process incoming messages
client.loop_forever()
