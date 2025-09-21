import time
import requests
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802

API_KEY = "YOUR_API_KEY"   # API key
URL = "https://api.thingspeak.com/update"

dht = DHT("22", 5)  # D5
lcd = JHD1802()

# --- Biến lưu dữ liệu ---
temps = []
hums = []

# --- Sent up data ThingSpeak ---
def send_to_thingspeak(temp_avg, hum_avg):
    try:
        payload = {
            "api_key": API_KEY,
            "field1": temp_avg,
            "field2": hum_avg
        }
        r = requests.get(URL, params=payload, timeout=5)
        if r.status_code == 200:
            print(f"[OK] Sent -> Temp:{temp_avg:.1f}C, Hum:{hum_avg:.1f}%")
        else:
            print("[ERR] ThingSpeak response:", r.status_code)
    except requests.exceptions.ConnectionError:
        print("[ERR] Không có kết nối mạng, thử lại lần sau...")
    except requests.exceptions.Timeout:
        print("[ERR] Hết thời gian chờ kết nối...")
    except Exception as e:
        print("[ERR] Lỗi khác:", e)

# --- Main ---
try:
    start_time = time.time()
    while True:
        hum, temp = dht.read()

        # Add data
        temps.append(temp)
        hums.append(hum)

        # Input value LCD 
        lcd.setCursor(0, 0)
        lcd.write(f"T:{temp:.1f} H:{hum:.1f}   ")

        # Mỗi 20s (10 lần đọc)
        if len(temps) >= 10:
            temp_avg = sum(temps) / len(temps)
            hum_avg = sum(hums) / len(hums)

            # Input value avg in LCD
            lcd.setCursor(1, 0)
            lcd.write(f"AvgT:{temp_avg:.1f} H:{hum_avg:.1f}   ")

            # Upload data ThingSpeak
            send_to_thingspeak(temp_avg, hum_avg)

            # Reset buffer
            temps.clear()
            hums.clear()

        # -- Delay 2s
        time.sleep(2)

except KeyboardInterrupt:
    print("Thoát chương trình")
    lcd.clear()

