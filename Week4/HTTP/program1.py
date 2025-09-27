import requests
import time
import random

# API key của ThingSpeak (Write API Key)
WRITE_API_KEY = "8TCXXRHS2MI50OIM"
URL = "https://api.thingspeak.com/update"

# Bộ nhớ tạm để lưu dữ liệu trong 20 giây
temps, hums, volts = [], [], []

start_time = time.time()
duration = 45 * 60  # chạy ít nhất 45 phút

while time.time() - start_time < duration:
    # Sinh dữ liệu random
    temp = random.uniform(20, 50)   # Nhiệt độ 20-50
    hum = random.uniform(20, 90)    # Độ ẩm 20-90
    volt = random.uniform(0, 3.3)   # Điện áp 0-3.3V

    # Lọc dữ liệu lỗi (giả sử <0 hoặc quá lớn là lỗi)
    if 0 <= temp <= 100 and 0 <= hum <= 100 and 0 <= volt <= 3.3:
        temps.append(temp)
        hums.append(hum)
        volts.append(volt)

    # Nếu đủ 20 giây thì tính trung bình và gửi
    if len(temps) >= 20:
        avg_temp = sum(temps) / len(temps)
        avg_hum = sum(hums) / len(hums)
        avg_volt = sum(volts) / len(volts)

        # Gửi dữ liệu qua HTTP
        payload = {
            "api_key": WRITE_API_KEY,
            "field1": avg_temp,
            "field2": avg_hum,
            "field3": avg_volt
        }
        r = requests.post(URL, params=payload)
        print(f"📤 Gửi: Temp={avg_temp:.2f}, Hum={avg_hum:.2f}, Volt={avg_volt:.2f}, Status={r.status_code}")

        # Reset mảng
        temps, hums, volts = [], [], []

    time.sleep(1)

