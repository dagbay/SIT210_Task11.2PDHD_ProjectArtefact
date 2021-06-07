from smbus import SMBus
from gpiozero import DistanceSensor, PWMLED
from time import sleep
from signal import SIGTERM, SIGHUP, pause, signal

# Setup
led = PWMLED(17) # LED
distance_sensor = DistanceSensor(echo=4, trigger=27) # Distance Sensor 
addr = 0x8 # Address of where the byte will be sent to.
bus = SMBus(1) # Uses Port I2C1
time_until_off = 60 # The time it takes until led turns off.

# Provides a safer way to exit the program.
def exit_safe():
    exit(1)

def start_timer():
    bus.write_byte(addr, 0x1) # Sends a single byte to the slave device which will turn on the in-built LED.
    led.on() # Turn on the LED
    bus.write_byte(addr, 0x2) # Sends another single byte to the slave device to avoid the IFTTT to send multiple notifications.
    sleep(time_until_off) # Sets a timer for 60 seconds.
    bus.write_byte(addr, 0x0) # Sends a single byte to the slave device which will turn off the in-built LED.
    led.off() # Turns of the LED.
    bus.write_byte(addr, 0x2) # Sends a single byte to the slave device which will do nothing.
                
def main():
    checking_status = True # This boolean variable is used for the while loop.
    has_entered = False # This boolean variable is used to see if the sensor has sensed a distance between something and itself below 1.
    try:
        signal(SIGTERM, exit_safe) # Termination Signal.
        signal(SIGHUP, exit_safe) # Hangup Signal.
        while checking_status:
            distance = distance_sensor.value # Float variable called distance is initialized to take in the value of the sensor.
            print(f'Distance(m): {distance:1.2f}') # The distance will be printed.
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
    finally:
        checking_status = False
        distance_sensor.close()
        led.off()

if __name__ == '__main__':
    main()
