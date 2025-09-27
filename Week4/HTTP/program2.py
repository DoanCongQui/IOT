import requests
import time
import csv

# API key để đọc (Read API Key)
READ_API_KEY = "28HN8TRMTLPQZNR2"
CHANNEL_ID = "3092104"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

# File log
log_file = "log_data.csv"

# Tạo file log nếu chưa có
with open(log_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Temperature", "Humidity", "Voltage", "LED_Red", "LED_Yellow", "LED_Green"])

while True:
    try:
        # Lấy dữ liệu mới nhất
        resp = requests.get(URL, params={"api_key": READ_API_KEY, "results": 1})
        data = resp.json()["feeds"][0]

        temp = float(data["field1"])
        hum = float(data["field2"])
        volt = float(data["field3"])

        # Điều khiển LED (hiển thị terminal)
        led_red = "ON" if temp > 40 else "OFF" if temp < 30 else "-"
        led_yellow = "ON" if hum > 70 else "OFF" if hum < 40 else "-"
        led_green = "ON" if volt > 2.0 else "OFF" if volt < 1.0 else "-"

        print(f"📥 Nhận: Temp={temp:.2f}, Hum={hum:.2f}, Volt={volt:.2f}")
        print(f"💡 LED: Red={led_red}, Yellow={led_yellow}, Green={led_green}")

        # Ghi log
        with open(log_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), temp, hum, volt, led_red, led_yellow, led_green])

    except Exception as e:
        print("⚠️ Lỗi:", e)

    time.sleep(1)

