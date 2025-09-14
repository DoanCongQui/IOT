import time
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO

def dieukhien_relay(nhietdo, relay, relay_onoff):
    if nhietdo > 40 and not relay_onoff:
        relay.write(1)
        return True, "R:ON "
    elif nhietdo < 30 and relay_onoff:
        relay.write(0)
        return False, "R:OFF"
    return relay_onoff, "R:ON " if relay_onoff else "R:OFF"

def capnhat_lcd(lcd, nhietdo, doam, relay_tt):
    lcd.setCursor(0, 0)
    lcd.write(' ' * 16)
    lcd.setCursor(1, 0)
    lcd.write(' ' * 16)

    lcd.setCursor(0, 0)
    lcd.write(f'N.do: {nhietdo:1}C')
    lcd.setCursor(1, 0)
    lcd.write(f'Doam: {doam:1}%')

    lcd.setCursor(0, 10)
    lcd.write(relay_tt)

# ------------------ Main ------------------
def main():
    lcd = JHD1802()
    cambien = DHT('11', 5)  
    relay = GPIO(22, GPIO.OUT)  

    relay_onoff = False

    while True:
        doam, nhietdo = cambien.read()
        print(f'Nhietdo: {nhietdo}C, Doam: {doam}%')
        
        relay_onoff, relay_tt = dieukhien_relay(nhietdo, relay, relay_onoff)
        if nhietdo > 40 and relay_onoff:
            print("Relay ON")
        elif nhietdo < 30 and not relay_onoff:
            print("Relay OFF")

        capnhat_lcd(lcd, nhietdo, doam, relay_tt)

        time.sleep(2)
        lcd.clear()

# ------------------ Run ------------------
if __name__ == "__main__":
    main()

