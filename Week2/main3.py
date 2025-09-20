import time
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO
from grove.adc import ADC
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

# --- Setup ---
adc = ADC()
dht = DHT("11", 5)   # DHT11 in D5
light_channel = 0     # Light A0
rotary_channel = 2    # Bien tro A2
ultrasonic = GroveUltrasonicRanger(16)   # Sieu am D16

# --- LCD ---
lcd = JHD1802()

# --- LED ---
led_red = GPIO(26, GPIO.OUT)    # D17
led_yellow = GPIO(24, GPIO.OUT) # D18
led_blue = GPIO(22, GPIO.OUT)   # D19

state_red = 0
state_yellow = 0
state_blue = 0

# Hien thi cac thong so ra lcd
def display_main(temp, hum, light, rotary_v, distance):
    lcd.setCursor(0, 0)
    lcd.write("T:{:d} H:{:d} D:{:.1f}".format(temp, hum, distance))
    lcd.setCursor(1, 0)
    lcd.write("L:{:d} V:{:.1f}".format(light, rotary_v))
    print(f"Temp={temp:.1f}C  Hum={hum:.1f}%  Light={light:.0f}  Rotary={rotary_v:.2f}V  Dist={distance:.1f}cm")

# Hien thi khi bat tat led
def display_led_status(name, value, status):
    msg = f"{name}:{'ON' if status else 'OFF'} Val={value:.2f}"
    print(msg)
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write(f"{name}:{'ON' if status else 'OFF'}")
    lcd.setCursor(1, 0)
    lcd.write(f"Val={value:.2f}")
    time.sleep(3) 
    lcd.clear()

# Tinh gai tri dien ap 
def read_rotary_voltage(channel):
    raw = adc.read(channel)
    return raw / 1023*3.3  # ADC 10bit

try:
    while True:
        hum, temp = dht.read()
        light = adc.read(light_channel)
        rotary_v = read_rotary_voltage(rotary_channel)
        distance = ultrasonic.get_distance()
        # --- Kiểm tra LED ---
        #  LED red
        if temp > 40 and state_red == 0:
            led_red.write(1)
            state_red = 1
            display_led_status("RED", temp, 1)
        elif temp < 30 and state_red == 1:
            led_red.write(0)
            state_red = 0
            display_led_status("RED", temp, 0)

        # LED yellow
        if hum > 70 and state_yellow == 0:
            led_yellow.write(1)
            state_yellow = 1
            display_led_status("YELLOW", hum, 1)
            
        elif hum < 40 and state_yellow == 1:
            led_yellow.write(0)
            state_yellow = 0
            display_led_status("YELLOW", hum, 0)

        # LED blue
        if rotary_v > 2.0 and state_blue == 0:
            led_blue.write(1)
            state_blue = 1
            display_led_status("BLUE", rotary_v, 1)
        elif rotary_v < 1.0 and state_blue == 1:
            led_blue.write(0)
            state_blue = 0
            display_led_status("BLUE", rotary_v, 0)

        # --- In ra man hinh ---
        lcd.clear()
        display_main(temp, hum, light, rotary_v, distance)

        time.sleep(1)

except KeyboardInterrupt:
    print("Thoát chương trình")
    led_red.write(0)
    led_yellow.write(0)
    led_blue.write(0)
    lcd.clear()

