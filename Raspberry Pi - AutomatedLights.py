from smbus import SMBus
from gpiozero import DistanceSensor, PWMLED
from time import sleep
from signal import SIGTERM, SIGHUP, pause, signal

# Setup
led = PWMLED(17)
distance_sensor = DistanceSensor(echo=4, trigger=27) # Distance Sensor 
addr = 0x8 # Address of where the byte will be sent to.
bus = SMBus(1) # Uses Port I2C1
time_until_off = 60 # The time it takes until led turns off.

num = 1

# Provides a safer way to exit the program.
def exit_safe():
    exit(1)

def start_timer():
    bus.write_byte(addr, 0x1) # Sends a single byte to the slave device which will turn on the in-built LED.
    led.on()
    bus.write_byte(addr, 0x2)
    sleep(time_until_off)
    bus.write_byte(addr, 0x0) # Sends a single byte to the slave device which will turn off the in-built LED.
    led.off()
    bus.write_byte(addr, 0x2) # Sends a single byte to the slave device which will do nothing.
                
def main():
    checking_status = True
    has_entered = False
    try:
        signal(SIGTERM, exit_safe) # Termination Signal.
        signal(SIGHUP, exit_safe) # Hangup Signal.
        while checking_status:
            distance = distance_sensor.value
            print(f'Distance(m): {distance:1.2f}')
            if distance < 0:
                distance = 0.00
            try:
                if distance < 1:
                    has_entered = True
                else: has_entered = False
            except:
                continue
            if has_entered:
                start_timer()
                
    except KeyboardInterrupt:
        bus.write_byte(addr, 0x0) # Sends a single byte to the slave device which will turn off the in-built LED if the Keyboard has been interrupted.
        led.off()
    finally:
        checking_status = False
        distance_sensor.close()

if __name__ == '__main__':
    main()