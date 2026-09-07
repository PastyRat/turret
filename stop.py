import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

arduino.write(b"END")  # Send the message to set all motors to 0