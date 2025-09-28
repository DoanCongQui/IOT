import time
import random
import threading
import requests
import paho.mqtt.client as mqtt
from grove.adc import ADC
from seeed_dht import DHT

# ==== CONFIG THINGSPEAK ====
CHANNEL_ID = "YOUR_CHANNEL_ID"
HTTP_API_KEY = "YOUR_HTTP_WRITE_API_KEY"   # Write API Key HTTP

# URL cho HTTP
HTTP_URL = f"https://api.thingspeak.com/update?api_key={HTTP_API_KEY}"

# Config cho MQTT
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "YOUR_MQTT_CLIENT_ID"
MQTT_USERNAME = MQTT_CLIENT_ID
MQTT_PASSWORD = "YOUR_MQTT_PASSWORD"
MQTT_TOPIC = f"channels/{CHANNEL_ID}/publish"

# Tao bien luu du lieu
avg_temp, avg_hum, avg_volt = 0, 0, 0
lock = threading.Lock()

adc = ADC()
dht = DHT("22", 5)  
rotary_channel = 0  

# Func doc bien tro votl
def read_rotary_voltage(channel):
    raw = adc.read(channel)  # 10-bit
    return raw / 1023 * 3.3

# Func doc cam bien return data sensor
def read_sensors():
    hum, temp = dht.read()
    volt = read_rotary_voltage(rotary_channel)
    return temp, hum, volt

def collect_data():
    global avg_temp, avg_hum, avg_volt
    while True:
        temps, hums, volts = [], [], []
        for _ in range(20):
            t, h, v = read_sensors()
            if 10 < t < 70:
                temps.append(t)
            if 20 < h < 100:
                hums.append(h)
            if 0 < v < 3.3:
                volts.append(v)
            time.sleep(1)

        with lock:
            avg_temp = sum(temps) / len(temps) if temps else 0
            avg_hum = sum(hums) / len(hums) if hums else 0
            avg_volt = sum(volts) / len(volts) if volts else 0


def send_http_and_mqtt():
    """Gửi HTTP tại giây 20 và MQTT tại giây 22"""
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    while True:
        time.sleep(20)  
        with lock:
            payload_http = {
                "field1": avg_temp,
                "field2": avg_hum
            }
        try:
            r = requests.post(HTTP_URL, data=payload_http, timeout=5)
            print(f"HTTP Sent -> Temp={avg_temp:.2f}, Hum={avg_hum:.2f}")
        except Exception as e:
            print("[HTTP] Error:", e)

        time.sleep(2) # Delay 2s
        with lock:
            msg = f"field3={avg_volt}"
        try:
            client.publish(MQTT_TOPIC, msg)
            print(f"QTT Sent -> Volt={avg_volt:.2f}")
        except Exception as e:
            print("[MQTT] Error:", e)


if __name__ == "__main__":
    # Create thread 
    t1 = threading.Thread(target=collect_data, daemon=True)
    t2 = threading.Thread(target=send_http_and_mqtt, daemon=True)

    # Start thread
    t1.start()
    t2.start()

