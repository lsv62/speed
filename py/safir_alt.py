import serial
import time
import struct
import math
import sys
import json

def read_sensor(port,command):
    try:
        # Send the command
        port.write(command)

        # Wait for a short time to ensure response is received
        time.sleep(0.1)

        # Read response (assuming response length is known)
        byte1 = port.read(1)  # Adjust the number of bytes to read based on your expected response length
        float1 = port.read(4)  # Adjust the number of bytes to read based on your expected response length
        end4 = port.read(4)  # Adjust the number of bytes to read based on your expected response length

        if len(float1) == 4:
            # Unpack bytes as Little-Endian 32-bit float
            measure = struct.unpack('<f', float1)[0]

            return measure

    except serial.SerialException:
        print("An error occurred while writing to the serial port.")   

# reads the JSON file and loads its content into a dictionary
def read_config(filename):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Failed to parse JSON in '{filename}'.")
        return None

def open_serial_port(config):
    try:
        ser = serial.Serial(**config)
        print("Serial port", config["port"], "opened successfully.")
        return ser
    except serial.SerialException:
        print("Failed to open serial port", config["port"])
        return None
    
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
read_static_pres = b'\x81\x7E'
read_temp = b'\x11\xEE'

try:

    press_config = read_config("press_config.json")
    if press_config:
        # Assigning a dictionary field to a variable
        ground_pressure = press_config['ground_level_pressure']
    
    abs_config = read_config("com_abs_config.json")
    if abs_config:
        abs_port = open_serial_port(abs_config)
    if abs_port:

        measured_pressure = read_sensor(abs_port,read_static_pres)
        print("Absolute pressure: {:.5f} Bar".format(measured_pressure))

        altitude = calculate_altitude(measured_pressure,ground_pressure)
        print("Altitude: {:.2f} km".format(altitude))

        measured_temperature = read_sensor(abs_port,read_temp)
        print("Temperature: {:.1f} Celsius degrees".format(measured_temperature))    

finally:
    # Close the serial port
    if abs_port.is_open:
        abs_port.close()
