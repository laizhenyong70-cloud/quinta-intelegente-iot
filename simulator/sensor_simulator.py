import time
import json
import random
from paho.mqtt import client as mqtt_client
BROKER_HOST = "127.0.0.1"
#BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "farm/data"
CLIENT_ID = "PigFarm_Simulator_001"

def run():
    "Create a transmitter and name it ""Pig Farm Simulator"
    # Tell it you are using the latest 2.0 version interface."
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, CLIENT_ID)
    try:
        # Connect to the Docker MQTT server you just set up
        client.connect(BROKER_HOST,BROKER_PORT)
        print("Connection successful! Now sending data to 1000 sensors...")

        while True:
            #The loop repeats 1000 times in an instant, simulating 10 devices reporting data in that single second.
            for i in range(1,10):
                payload = {
                    "sensor_id": f"SN-{i:04d}",
                    "temperature": round(random.uniform(22.0,35.0),2),
                    "humidity": round(random.uniform(35,100),2),
                    "nh3": round(random.uniform(0,10),2),
                    "status":"normal",
                    "timestamp":time.strftime("%Y-%m-%d %H:%M:%S")
                }
                #sent to farm/data
                result = client.publish(TOPIC,json.dumps(payload))
                print(result.rc)
            print(f"One round of reporting completed: 1000 data entries have been fed into the pipeline | Time:{time.strftime('%H:%M:%S')}")
            time.sleep(10)
    except Exception as e:
        print(f"conect failed: {e},please check")
if __name__ == "__main__":
    run()
        