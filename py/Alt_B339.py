import serial
import time
import struct
import math
import json
import sys


# Define the desired period in seconds (10 milliseconds = 0.01 seconds)
period = 0.0625

def read_sensor(port):
    try:

        # Wait for a short time to ensure response is received
        # time.sleep(0.1)

        # Read response (assuming response length is known)
        byte1 = port.read(1)  # Adjust the number of bytes to read based on your expected response length
        float1 = port.read(4)  # Adjust the number of bytes to read based on your expected response length
        end4 = port.read(4)  # Adjust the number of bytes to read based on your expected response length

        if byte1:
            print("byte1:",hex(ord(byte1)), " ", end='')   

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
reset = b'\x01\xFE'
read_temp = b'\x11\xEE'
last_time = 0

try:

    press_config = read_config("press_config.json")
    if press_config:
        # Assigning a dictionary field to a variable
        ground_pressure = press_config['ground_level_pressure']
    
    abs_config = read_config("com_abs_config.json")
    if abs_config:
        abs_port = open_serial_port(abs_config)
    if abs_port:
        # Send the command
        abs_port.write(read_static_pres)
        time.sleep(period)
        start_time = time.time() #get current time
        while True:
            meas_time = time.time() #get current time
            elapsed_time =  meas_time - last_time # Calculate elapsed time since lust measurement
            if elapsed_time > period:
                # Add other processing or logic here if needed
                meas_pressure = read_sensor(abs_port)

                print("Period: {:.3f}s, Time: {:.3f}".format(elapsed_time, meas_time-start_time), end='')
                if (meas_pressure):
                    print(" Abs_pressure: {:.7f} Bar".format(meas_pressure), end='')
                    altitude = calculate_altitude(meas_pressure,ground_pressure)
                    print(" Altitude: {:.2f} km".format(altitude), flush=True)
                else:
                    print("", flush=True)
                    file_path = 'test_result.txt'
                    # Opening 'example.txt' in append mode
                    with open(file_path, 'a') as file:
                        file.write("Period: {:.3f}s, Time: {:.3f}\n".format(elapsed_time, meas_time-start_time))
                    break  # Breaks out of the while loop

    # You can write more lines or perform other operations on the file within this block

# File is automatically closed outside the 'with' block

                last_time = meas_time

                # Send the command
                abs_port.write(read_static_pres)
        
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")
    # Optionally, perform cleanup or final actions here

    # Exit the program gracefully
    sys.exit(0)  # Import sys module if not already imported

finally:
    # Close the serial port
    if abs_port.is_open:
        abs_port.close()
