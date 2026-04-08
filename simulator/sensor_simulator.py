import time
import json
import random
from paho.mqtt import client as mqtt_client
from weather_ref import fetch_lisbon_weather
from datetime import datetime

BROKER_HOST = "127.0.0.1"
#BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "farm/data"
CLIENT_ID = "PigFarm_Simulator_001"

def generate_sensor_data() -> dict:
    weather = fetch_lisbon_weather()

    outside_temperature = weather["outside_temperature"]
    outside_humidity = weather["outside_humidity"]

    now = datetime.now()
    hour = now.hour

    # 猪舍内部相对室外会稍微暖一点，湿一点
    temp_offset = 1.5
    humidity_offset = 4.0

    #根据一天中时间段调整温湿度
    if 0 <= hour <= 6:
        temp_day_adjust = -1.0
    elif 7 <= hour <= 10:
        temp_day_adjust = -0.3
    elif 11 <= hour <= 16:
        temp_day_adjust = 1.2
    elif 17 <= hour <= 21:
        temp_day_adjust = 0.2
    else:
        temp_day_adjust = -0.6
    
    #最终室外温度 = 室外温度 + 猪舍温度偏移 + 小随机扰动
    temperature = temperature = outside_temperature + temp_offset + temp_day_adjust + random.uniform(-0.5, 0.5)

    # 最终湿度 = 室外参考 + 猪舍偏移 + 小随机扰动
    humidity = outside_humidity + humidity_offset + random.uniform(-3.0, 3.0)

    # 限制范围，避免数据太夸张
    temperature = round(max(16.0, min(32.0, temperature)), 1)
    humidity = round(max(35.0, min(90.0, humidity)), 1)

     # NH3 做一点轻微联动
    nh3 = 8 + (humidity - 50) * 0.08 + random.uniform(-1.0, 1.5)
    nh3 = round(max(5.0, min(30.0, nh3)), 1)

    status = "normal"
    if temperature > 30 or humidity > 85 or nh3 > 25:
        status = "warning"
    return{
        "sensor_id": "SN-0001",
        "temperature": temperature,
        "humidity": humidity,
        "nh3": nh3,
        "status":status,
        "timestamp":now.strftime("%Y-%m-%d %H:%M:%S")
    }


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
            # for i in range(1,10):
            #     payload = {
            #         "sensor_id": f"SN-{i:04d}",
            #         "temperature": round(random.uniform(22.0,35.0),2),
            #         "humidity": round(random.uniform(35,100),2),
            #         "nh3": round(random.uniform(0,10),2),
            #         "status":"normal",
            #         "timestamp":time.strftime("%Y-%m-%d %H:%M:%S")
            #     }
            payload = generate_sensor_data()
            print(payload)
            #sent to farm/data
            result = client.publish(TOPIC,json.dumps(payload))
            print(result.rc)
            print(f"One round of reporting completed: 1000 data entries have been fed into the pipeline | Time:{time.strftime('%H:%M:%S')}")
            time.sleep(10)
    except Exception as e:
        print(f"conect failed: {e},please check")
if __name__ == "__main__":
    run()
        