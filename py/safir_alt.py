import serial
import time
import struct
import math
import sys
    
def calculate_altitude(pressure, ground_level_pressure=1.01325):
    # Constants
    L = 0.0065  # Temperature lapse rate (K/m)
    T0 = 288.15  # Standard temperature at sea level (K)
    g = 9.80665  # Acceleration due to gravity (m/s^2)
    M = 0.0289644  # Molar mass of Earth's air (kg/mol)
    R = 8.31447  # Universal gas constant (J/(mol·K))
    
    # Calculate altitude using barometric formula
    altitude = ((T0 / L) * (1 - (pressure / ground_level_pressure)**((R * L) / (g * M)))) / 1000.0  # Convert to kilometers
    
    return altitude

# Define the command to send (hexadecimal representation of ASCII characters)
command = b'\x81\x7E'

# Configure the serial port
ser = serial.Serial('COM5', 115200, timeout=1)  # Adjust baud rate and timeout as needed

try:
    # Open the serial port
    if not ser.is_open:
        ser.open()

    # Send the command
    ser.write(command)

    # Wait for a short time to ensure response is received
    time.sleep(0.1)

    # Read response (assuming response length is known)
    byte1 = ser.read(1)  # Adjust the number of bytes to read based on your expected response length
    float1 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length
    end4 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length
        
    if __name__ == "__main__":
        # Check if the expected number of command-line arguments is provided
        if len(sys.argv) != 2:
            print("Usage: python script.py <float_value>")
            sys.exit(1) 

        ground_pressure = float(sys.argv[1])
        print("ground pressure:", ground_pressure)

    if len(float1) == 4:
        # Unpack bytes as Little-Endian 32-bit float
        measured_pressure = struct.unpack('<f', float1)[0]
        print("Absolute pressure:", measured_pressure)

    altitude = calculate_altitude(measured_pressure,ground_pressure)
    print("Altitude: {:.2f} km".format(altitude))
finally:
    # Close the serial port
    if ser.is_open:
        ser.close()
