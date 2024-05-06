import serial
import time
import struct
import math
import sys

def calculate_airspeed(delta_p, atm_pressure=1.00, temp_celsius=15.0):
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
read_pres = b'\x84\x7B'
read_temp = b'\x14\xEB'
read_static_pres = b'\x81\x7E'

# Configure the pressure drop serial port
ser = serial.Serial('COM6', 115200, timeout=1)  # Adjust baud rate and timeout as needed

try:
        
    if __name__ == "__main__":
        # Check if the expected number of command-line arguments is provided
        if len(sys.argv) != 2:
            pressure_drop_offset=0
            print("Usage: default ground pressure")
        elif len(sys.argv) == 2: 
            pressure_drop_offset = float(sys.argv[1])

    # Open the serial port
    if not ser.is_open:
        ser.open()

    # Send the command
    ser.write(read_pres)

    # Wait for a short time to ensure response is received
    time.sleep(0.1)

    # Read response (assuming response length is known)
    byte1 = ser.read(1)  # Adjust the number of bytes to read based on your expected response length
    float1 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length
    end4 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length

    if len(float1) == 4:
        # Unpack bytes as Little-Endian 32-bit float
        measured_pressure_drop = struct.unpack('<f', float1)[0]
        print("Measured_pressure_drop: {:.4f} Bar".format(measured_pressure_drop))

    # Send the command
    ser.write(read_temp)

    # Wait for a short time to ensure response is received
    time.sleep(0.1)

    # Read response (assuming response length is known)
    byte1 = ser.read(1)  # Adjust the number of bytes to read based on your expected response length
    float1 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length
    end4 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length

    if len(float1) == 4:
        # Unpack bytes as Little-Endian 32-bit float
        measured_temperature = struct.unpack('<f', float1)[0]
        print("Measured_temperature: {:.2f} degrees Celsius".format(measured_temperature))


    # Close the serial port
    if ser.is_open:
        ser.close()

    # Configure the static pressure sensor serial port
    ser = serial.Serial('COM5', 115200, timeout=1)  # Adjust baud rate and timeout as needed

   # Open the serial port
    if not ser.is_open:
        ser.open()

    # Send the command
    ser.write(read_static_pres)

    # Wait for a short time to ensure response is received
    time.sleep(0.1)

    # Read response (assuming response length is known)
    byte1 = ser.read(1)  # Adjust the number of bytes to read based on your expected response length
    float1 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length
    end4 = ser.read(4)  # Adjust the number of bytes to read based on your expected response length

    if len(float1) == 4:
        # Unpack bytes as Little-Endian 32-bit float
        measured_pressure = struct.unpack('<f', float1)[0]
        print("Absolute pressure: {:.6f} Bar".format(measured_pressure))

    dp = measured_pressure_drop-pressure_drop_offset

    if dp<0:
        dp=0

    result_airspeed = calculate_airspeed(dp, measured_pressure, measured_temperature)
    print("Airspeed: {:.2f} m/s".format(result_airspeed))

finally:
    # Close the serial port
    if ser.is_open:
        ser.close()
