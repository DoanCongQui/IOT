import paho.mqtt.client as mqtt
import csv
from datetime import datetime

# ========== CẤU HÌNH ==========
CHANNEL_ID = "3092104"
CLIENT_ID = "BTUwPBwEBgQnJiYhGyIxLgY"
USERNAME = CLIENT_ID
PASSWORD = "ihAI+gTyh5IIuYI0c7+xuD1P"

BROKER = "mqtt3.thingspeak.com"
PORT = 1883
TOPIC = f"channels/{CHANNEL_ID}/subscribe/fields/+"

log_file = "program2_log.csv"

with open(log_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Temp", "Humidity", "Voltage"])

# Biến lưu tạm giá trị nhận được
latest_temp = None
latest_hum = None
latest_volt = None

# ========== CALLBACK ==========
def on_connect(client, userdata, flags, rc):
    print("✅ Đã kết nối MQTT, code:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global latest_temp, latest_hum, latest_volt
    value = msg.payload.decode().strip()
    topic = msg.topic

    try:
        if "field1" in topic:
            latest_temp = float(value)
        elif "field2" in topic:
            latest_hum = float(value)
        elif "field3" in topic:
            latest_volt = float(value)

        # Chỉ khi đã có đủ 3 giá trị thì mới in/log
        if latest_temp is not None and latest_hum is not None and latest_volt is not None:
            print(f"🌡 Temp={latest_temp}°C, 💧 Hum={latest_hum}%, 🔋 Volt={latest_volt}V")

            # Điều khiển LED (in ra terminal)
            if latest_temp > 40:
                print("🔴 LED Đỏ: BẬT (nhiệt độ > 40)")
            elif latest_temp < 30:
                print("🔴 LED Đỏ: TẮT (nhiệt độ < 30)")

            if latest_hum > 70:
                print("🟡 LED Vàng: BẬT (độ ẩm > 70%)")
            elif latest_hum < 40:
                print("🟡 LED Vàng: TẮT (độ ẩm < 40%)")

            if latest_volt > 2.0:
                print("🟢 LED Xanh: BẬT (volt > 2.0V)")
            elif latest_volt < 1.0:
                print("🟢 LED Xanh: TẮT (volt < 1.0V)")

            # Ghi log
            with open(log_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().isoformat(), latest_temp, latest_hum, latest_volt])

    except Exception as e:
        print("⚠️ Lỗi parse:", e)

# ========== MAIN ==========
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()

