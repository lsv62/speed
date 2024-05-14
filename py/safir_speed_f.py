import serial
import time
import struct
import math
import json
import datetime

# File path where you want to save the pressure data
file_path = 'data.txt'

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
read_static_temp = b'\x11\xEE'
read_static_pres = b'\x81\x7E'

try:
    press_config = read_config("press_config.json")
    if press_config:
        # Assigning a dictionary field to a variable
        pressure_drop_offset = press_config['drop_offset']

    abs_config = read_config("com_abs_config.json")
    if abs_config:
        abs_port = open_serial_port(abs_config)

    diff_config = read_config("com_diff_config.json")
    if diff_config:
        diff_port = open_serial_port(diff_config)

    if abs_port:
        abs_pressure = read_sensor(abs_port,read_static_pres)
        print("Absolute pressure: {:.5f} Bar".format(abs_pressure))

        stat_temperature = read_sensor(abs_port,read_static_temp)
        print("Static Temperature: {:.1f} Celsius degrees".format(stat_temperature))

    if diff_port:
            pressure_drop = read_sensor(diff_port,read_drop)
            print("Measured_drop: {:.5f} Bar".format(pressure_drop))

            drop_temperature = read_sensor(diff_port,read_temp)
            print("Drop_temperature: {:.2f} degrees Celsius".format(drop_temperature))

    IAS = calculate_airspeed(pressure_drop,abs_pressure,drop_temperature)
    print("IAS: {:.2f} m/s".format(IAS))

    dp = pressure_drop-pressure_drop_offset
    if dp<0:
        dp=0

    CAS = calculate_airspeed(dp,abs_pressure,drop_temperature)
    print("CAS = TAS: {:.2f} m/s".format(CAS))

    EAS = calculate_airspeed(dp)
    print("EAS: {:.2f} m/s".format(EAS))

# Open file for writing
with open(file_path, 'a') as file:

    # Write each pressure reading with timestamp to the file
    timestamp = datetime.datetime.now().isoformat()
    file.write(f'{timestamp} Abs_Pres={abs_pressure} Pa') # Write timestamp and pressure value
    file.write(f' Drop={pressure_drop}(Pa) Drop_temp={drop_temperature}(C)')
    file.write(f' IAS={IAS}(m/s) CAS={CAS}(m/s) EAS={EAS}(m/s)\n')

finally:
    # Close the serial ports
    if abs_port.is_open:
        abs_port.close()
    if diff_port.is_open:
        diff_port.close()
