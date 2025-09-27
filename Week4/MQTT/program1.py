import time
import random
import requests
import paho.mqtt.client as mqtt
import csv
from datetime import datetime

# ========== CẤU HÌNH ==========
CHANNEL_ID = "3092104"  # Thay bằng Channel ID
WRITE_API_KEY = "8TCXXRHS2MI50OIM"  # Thay bằng Write API Key của bạn

# MQTT
BROKER = "mqtt3.thingspeak.com"
PORT = 1883
CLIENT_ID = "BTUwPBwEBgQnJiYhGyIxLgY"
USERNAME = CLIENT_ID
PASSWORD = "ihAI+gTyh5IIuYI0c7+xuD1P"
TOPIC = f"channels/{CHANNEL_ID}/publish"

# Tạo MQTT client
mqtt_client = mqtt.Client(client_id=CLIENT_ID)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

# File log
log_file = "program1_log.csv"

with open(log_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Temp", "Humidity", "Voltage"])

# ========== CHƯƠNG TRÌNH CHÍNH ==========
data_temp, data_hum, data_volt = [], [], []
start_time = time.time()

while True:
    # Giả lập dữ liệu đọc cảm biến
    temp = round(random.uniform(25, 45), 2)
    hum = round(random.uniform(30, 80), 2)
    volt = round(random.uniform(0.5, 3.3), 2)

    # Loại bỏ giá trị lỗi (ví dụ ngoài range hợp lệ)
    if not (0 <= temp <= 100 and 0 <= hum <= 100 and 0 <= volt <= 5):
        continue

    data_temp.append(temp)
    data_hum.append(hum)
    data_volt.append(volt)

    # Ghi log mỗi lần đọc
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), temp, hum, volt])

    # Sau mỗi 20 giây thì tính trung bình và gửi
    if time.time() - start_time >= 20:
        avg_temp = round(sum(data_temp)/len(data_temp), 2)
        avg_hum = round(sum(data_hum)/len(data_hum), 2)
        avg_volt = round(sum(data_volt)/len(data_volt), 2)

        print(f"📊 Gửi trung bình: Temp={avg_temp}, Hum={avg_hum}, Volt={avg_volt}")

        # Gửi HTTP
        url = f"https://api.thingspeak.com/update?api_key={WRITE_API_KEY}&field1={avg_temp}&field2={avg_hum}&field3={avg_volt}"
        requests.get(url)

        # Gửi MQTT
        payload = f"field1={avg_temp}&field2={avg_hum}&field3={avg_volt}"
        mqtt_client.publish(TOPIC, payload)

        # Reset
        data_temp, data_hum, data_volt = [], [], []
        start_time = time.time()

    time.sleep(1)

