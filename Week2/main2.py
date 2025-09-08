import time
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO

# ------------------ Điều khiển relay ------------------
def dieukhien_relay(nhietdo, relay, relay_onoff):
    if nhietdo > 40 and not relay_onoff:
        relay.write(1)
        return True, "R:ON "
    elif nhietdo < 30 and relay_onoff:
        relay.write(0)
        return False, "R:OFF"
    return relay_onoff, "R:ON " if relay_onoff else "R:OFF"

# ------------------ Cập nhật LCD ------------------
def capnhat_lcd(lcd, nhietdo, doam, relay_tt):
    # Xóa màn hình
    lcd.setCursor(0, 0)
    lcd.write(' ' * 16)
    lcd.setCursor(1, 0)
    lcd.write(' ' * 16)

    # Hiển thị giá trị
    lcd.setCursor(0, 0)
    lcd.write(f'Nhietdo: {nhietdo:3}C')
    lcd.setCursor(1, 0)
    lcd.write(f'Doam: {doam:4}%')

    lcd.setCursor(0, 10)
    lcd.write(relay_tt)

# ------------------ Main ------------------
def main():
    lcd = JHD1802()
    cambien = DHT('11', 5)  # cảm biến DHT11, chân D5
    relay = GPIO(12, GPIO.OUT)  # relay nối chân D12

    relay_onoff = False

    while True:
        # Đọc dữ liệu cảm biến
        doam, nhietdo = cambien.read()
        print(f'Nhietdo: {nhietdo}C, Doam: {doam}%')

        # Điều khiển relay
        relay_onoff, relay_tt = dieukhien_relay(nhietdo, relay, relay_onoff)
        if nhietdo > 26 and not relay_onoff:
            print("Relay ON")
        elif nhietdo < 25 and relay_onoff:
            print("Relay OFF")

        # Cập nhật LCD
        capnhat_lcd(lcd, nhietdo, doam, relay_tt)

        time.sleep(2)
        lcd.clear()

# ------------------ Run ------------------
if __name__ == "__main__":
    main()

