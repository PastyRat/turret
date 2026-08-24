import serial
import time

arduino = None

# Start connection to Arduino and stop program if we can't
def startconnection():
    global arduino
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)
        return 1
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return 0


def send(xzangle, finalangle):
    # Send the angles to the Arduino
    arduino.write(f"{xzangle},{finalangle}".encode())
    print(f"Sent angles: {xzangle}, {finalangle}")
    while True:
        line = arduino.readline().decode('utf-8').rstrip()
        print(line)
        if line == "Done":
            break
if __name__ == "__main__":
    # Example usage
    xzangle = 45.0  # Replace with your calculated xz angle
    finalangle = 30.0  # Replace with your calculated final angle
    send(xzangle, finalangle)
