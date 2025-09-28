import requests
import time
import csv
from gpiozero import LED
from grove.display.jhd1802 import JHD1802

# ----------------------- CONFIG -------------------------------
READ_API_KEY = "READ_API_KEY"   # Read API Key
CHANNEL_ID = "ID"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

# LCD Grove JHD1802 (I2C)
lcd = JHD1802()

# LED GPIO
led_red = LED(22)     # D17
led_yellow = LED(24)  # D18
led_blue = LED(26)    # D19

# File log
log_file = "data_log.csv"

# Setup file log
with open(log_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Temperature", "Humidity", "Voltage", "LED_Red", "LED_Yellow", "LED_Blue"])

# Dieu khien led
def led_control(temp_max, temp_min, hum_max, hum_min, volt_max, volt_min):
    if temp > temp_max:
        led_red.on()
        led_red_state = "ON"
    elif temp < temp_min:
        led_red.off()
        led_red_state = "OFF"
    else:
        led_red_state = "-"

    if hum > hum_max:
        led_yellow.on()
        led_yellow_state = "ON"
    elif hum < hum_min:
        led_yellow.off()
        led_yellow_state = "OFF"
    else:
        led_yellow_state = "-"

    if volt > volt_max:
        led_blue.on()
        led_blue_state = "ON"
    elif volt < volt_min:
        led_blue.off()
        led_blue_state = "OFF"
    else:
        led_blue_state = "-"

# ----------------- MAIN ----------------------------- 
while True:
    try:
        # Read data tu ThingSpeak
        resp = requests.get(URL, params={"api_key": READ_API_KEY, "results": 1}, timeout=5)
        js = resp.json()

        # Check data ?
        if "feeds" in js and len(js["feeds"]) > 0:
            feed = js["feeds"][0]

            temp = float(feed.get("field1", 0) or 0)
            hum = float(feed.get("field2", 0) or 0)
            volt = float(feed.get("field3", 0) or 0)
        else:
            print("No data")
            time.sleep(2)
            continue

        # Dieu khien led
        led_control(40, 30, 70, 40, 2, 1)

        # Hien thi Terminal
        print(f"Temp={temp:.2f}°C, Hum={hum:.2f}%, Volt={volt:.2f}V")
        print(f"LED: Red={led_red_state}, Yellow={led_yellow_state}, Blue={led_blue_state}")

        # Hien thi LCD
        lcd.setCursor(0, 0)
        lcd.write(f"T:{temp:.1f}C H:{hum:.1f}%   ")
        lcd.setCursor(1, 0)
        lcd.write(f"V:{volt:.2f}V")

        # Ghi log
        with open(log_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), temp, hum, volt,
                             led_red_state, led_yellow_state, led_blue_state])

    except Exception as e:
        print("Error:", e)

    time.sleep(1)

