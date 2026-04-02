import json
from paho.mqtt import client as mqtt_client

from database import init_db,insert_sensor_data
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "farm/data"
CLIENT_ID = "PigFarm_Server_001"

def on_connect(client,userdata,flags,reason_code,properties):
    if reason_code == 0:
        print("Connectes to MQTT broker sucessfully.")
        client.subscribe(TOPIC)
        print(f"Subscrited to topic:{TOPIC}")
    else:
        print(f"Failed to conect to MQTT broker,reasom code:{reason_code}")
def on_message(client,userdata,msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received message: {payload}") 



        sensor_id = payload["sensor_id"]
        temperature = payload["temperature"]
        humidity = payload["humidity"]
        nh3 = payload["nh3"]
        status = payload["status"]
        timestamp = payload["timestamp"] 

        insert_sensor_data(
            sensor_id=sensor_id,
            temperature=temperature,
            humidity=humidity,
            nh3=nh3,
            status=status,
            timestamp=timestamp,
        )
        print(f"Saved data for sensor {sensor_id}")

    except Exception as e:
        print(f"Error [rocessing message: {e}]")


def run():
    init_db()


    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        CLIENT_ID
    )
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER_HOST,BROKER_PORT)
        client.loop_forever()
    except Exception as e:
        print(f"Server failed to start: {e}")

if __name__ == "__main__":
    run()