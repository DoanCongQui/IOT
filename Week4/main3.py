import paho.mqtt.client as mqtt
import random
import time

# Cấu hình MQTT ThingSpeak
BROKER = "mqtt3.thingspeak.com"
PORT = 1883
CLIENT_ID = "BTUwPBwEBgQnJiYhGyIxLgY"   # Client ID
USERNAME = "BTUwPBwEBgQnJiYhGyIxLgY"   # Giống Client ID
PASSWORD = "ihAI+gTyh5IIuYI0c7+xuD1P"  # Password thật
CHANNEL_ID = "3092104"  # Channel ID của bạn

TOPIC = f"channels/{CHANNEL_ID}/publish"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Kết nối MQTT tới ThingSpeak thành công!")
    else:
        print("❌ Lỗi kết nối:", rc)

# Tạo client MQTT
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # Random dữ liệu giả
        nhiet_do = round(random.uniform(25, 40), 2)
        do_am = round(random.uniform(40, 80), 2)

        # Gửi dữ liệu lên field1 và field2
        payload = f"field1={nhiet_do}&field2={do_am}"
        client.publish(TOPIC, payload)
        print(f"📤 Gửi dữ liệu: {payload}")

        time.sleep(20)  # gửi mỗi 20 giây (theo giới hạn ThingSpeak)

except KeyboardInterrupt:
    print("🛑 Dừng chương trình")
    client.loop_stop()
    client.disconnect()

