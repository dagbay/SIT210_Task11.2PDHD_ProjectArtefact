#include <Wire.h>

int led = D7; // The in-built LED.
char c = '\u0000';

void setup() {
    Wire.begin(0x8); // Set slave device address as 0x8.
    Wire.onReceive(receiveEvent); // Receives data sent by the master.
    pinMode(led, OUTPUT); // Sets the LED as output.
    digitalWrite(led, LOW); // Sets the LED off.
}

void receiveEvent(int amount) { 
    while (Wire.available()) { // While the connection is available.
        c = Wire.read(); // Variable c will read from its master.
        if (c == 1 || c == 0) {
            digitalWrite(led, c); // The LED will take in the byte sent by the master to either turn on or off.
        }
    }
}

void sendNotification() {
    // If the data received from the master is equal 1 then this device will publish an event which will act as a notification for the user to receive.
    // To know if someone has entered the room or not.
    if (c == 1) {
        Particle.publish("sensor", "enabled", PRIVATE);
    }
    else if (c == 0) {
        Particle.publish("sensor", "disabled", PRIVATE);
    } else {
        Particle.publish("sensor", "none_detected", PRIVATE)
    }
}

void loop() {
    sendNotification();
}