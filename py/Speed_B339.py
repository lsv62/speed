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
    
def calculate_airspeed(delta_p, atm_pressure=1.01325, temp_celsius=15.0):
    # Constants
    gas_constant = 287.0  # Specific gas constant for dry air (J/(kg·K))

    # Convert temperature from Celsius to Kelvin
    temp_kelvin = temp_celsius + 273.15  # Convert Celsius to Kelvin

    # Calculate air density (rho) using ideal gas law
    air_density = atm_pressure / (gas_constant * temp_kelvin)

    # Calculate airspeed using the formula: V = sqrt((2 * delta_p) / rho)
    airspeed = math.sqrt((2 * delta_p) / air_density)

    return airspeed

# Define the command to send (hexadecimal representation of ASCII characters)
read_drop = b'\x84\x7B'
read_temp = b'\x14\xEB'
last_time = 0

try:

    press_config = read_config("press_config.json")
    if press_config:
        # Assigning a dictionary field to a variable
        pressure_drop_offset = press_config['drop_offset']
    
    diff_config = read_config("com_diff_config.json")
    if diff_config:
        diff_port = open_serial_port(diff_config)

    if diff_port:
        # Send the command
        diff_port.write(read_drop)
        time.sleep(period)
        start_time = time.time() #get current time
        while True:
            meas_time = time.time() #get current time
            elapsed_time =  meas_time - last_time # Calculate elapsed time since lust measurement
            if elapsed_time > period:
                # Add other processing or logic here if needed
                pressure_drop = read_sensor(diff_port)

                print("Period: {:.3f}s, Time: {:.3f}".format(elapsed_time, meas_time-start_time), end='')
                if (pressure_drop):
                    print(" diff_pressure: {:.7f} Bar".format(meas_pressure), end='')
                    dp = pressure_drop-pressure_drop_offset
                    if dp<0:
                        dp=0

                    EAS = calculate_airspeed(dp)

                    print(" EAS: {:.2f} km".format(altitude), flush=True)
                else:
                    print("", flush=True)
                    file_path = 'test_speed_result.txt'
                    # Opening 'example.txt' in append mode
                    with open(file_path, 'a') as file:
                        file.write("Sensor not answered in period: {:.3f}s by time: {:.3f}\n".format(elapsed_time, meas_time-start_time))
                    break  # Breaks out of the while loop

    # You can write more lines or perform other operations on the file within this block

# File is automatically closed outside the 'with' block

                last_time = meas_time

                # Send the command
                diff_port.write(read_drop)
        
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")
    # Optionally, perform cleanup or final actions here

    # Exit the program gracefully
    sys.exit(0)  # Import sys module if not already imported

finally:
    # Close the serial port
    if diff_port.is_open:
        diff_port.close()
