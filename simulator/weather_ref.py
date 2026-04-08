import requests
from datetime import datetime

LISBON_LAT = 38.7223
LISBON_LON = -9.1393


def fallback_weather() -> dict:
    """当天气接口失败时，使用本地默认值"""
    hour = datetime.now().hour

    if 0 <= hour <= 6:
        temperature = 15.0
        humidity = 70.0
    elif 7 <= hour <= 11:
        temperature = 18.0
        humidity = 60.0
    elif 12 <= hour <= 16:
        temperature = 19.0
        humidity = 58.0
    else:
        temperature = 16.5
        humidity = 65.0

    return {
        "outside_temperature": temperature,
        "outside_humidity": humidity,
        "source": "fallback"
    }


def fetch_lisbon_weather() -> dict:
    """获取里斯本当前天气"""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={LISBON_LAT}"
            f"&longitude={LISBON_LON}"
            "&current=temperature_2m,relative_humidity_2m"
            "&timezone=auto"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]

        return {
            "outside_temperature": float(current["temperature_2m"]),
            "outside_humidity": float(current["relative_humidity_2m"]),
            "source": "api"
        }

    except Exception as e:
        print(f"weather API failed: {e}")
        return fallback_weather()


if __name__ == "__main__":
    weather = fetch_lisbon_weather()
    print(weather)



# import requests
# from datetime import datetime

# LISBON_LAT = 38.7223
# LISBON_LON = -9.1393

# def fallback_weather()->dict:
#     """获取当天接口失败时，使用本地默认值"""
#     hour = datetime.now().hour

#     if 0 <= hour <= 6:
#         temperature = 15.0
#         humidity = 70.0
#     elif 7 <= hour <= 11:
#         temperature = 18
#         humidity = 60.0
#     elif 12 <= hour <= 16:
#         temperature = 19.0
#         humidity = 58.0
#     else :
#         temperature = 16.5
#         humidity = 65.0
#     return {
#         "outside_temperature":temperature,
#         "outside_humidity":humidity,
#         "source":"fallback"
#     }

# def fetch_lisbon_weather() ->dict:
#     """获取里斯本当前小时的室外温度和湿度"""
   
#     try:
#         url = (
#             "https://api.open-meteo.com/v1/forecast"
#             "?latitude=38.72"
#             "&longitude=-9.14"
#             "&hourly=temperature_2m,relative_humidity_2m"
#             "&timezone=auto"
#         )


#         response = requests.get(url,timeout=10)
#         response.raise_for_status()
#         data = response.json()

#         hourly = data["hourly"]
#         times = hourly["time"]
#         temperatures = hourly["temperature_2m"]
#         humidities = hourly["relative_humidity_2m"]

#         """current_hour = datetime.now().strftime("%Y-%m-%dt%H:00")
#         times = data["hourly"]["time"]
#         temperatures = data["hourly"]["temperature_2m"]
#         humidities = data["hourly"]["relative_humidity_2m"]"""

#         now_hour = datetime.now().strftime("%Y-%m-%dT%H:00")
#         if now_hour in times:
#             idx = times.index(now_hour)
#         else :
#             idx = 0
#         return {
#             "outside_temperature":float(temperatures[idx]),
#             "outside_humidity":float(humidities[idx]),
#             "source":"api"
#         }
#     except Exception as e:
#         print(f"weather API failed :{e}")
#         return fallback_weather()
# if __name__ == "__main__":
#     weather = fetch_lisbon_weather()
#     print(weather)
