import serial
import sys
import struct
import time

# Configure the serial port
ser = serial.Serial('COM4', 9600, timeout=1)  # Adjust 'COM1' and 9600 to your serial port and baudrate

# State machine variables
state = 0  # 0: Waiting for 'xAA', 1: Waiting for 'x55'

try:
    r_time = time.time() #get current time
    while True:
        # Read one byte from the serial port
        byte = ser.read(1)
        hex = byte.hex()
        if byte:
            # State machine logic

            if state == 0:
                if hex == 'aa':
                    state = 1
                    old_time = r_time
                    r_time = time.time() #get current time
            elif state == 1:
                if hex == '55':
                    
                    # Reset state to wait for next sequence
                    state = 0
                    float1 = ser.read(4)
                    float2 = ser.read(4)
                    # Unpack bytes as Little-Endian 32-bit float
                    pressure = struct.unpack('<f', float1)[0]
                    temperature = struct.unpack('<f', float2)[0]
                    print("Period: ", r_time-old_time, end='')
                    print(" Pressure: ", pressure, end='')
                    print(" Temprature: ", temperature, flush=True)

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")
    # Optionally, perform cleanup or final actions here

    # Exit the program gracefully
    sys.exit(0)  # Import sys module if not already imported

finally:
    # Close the serial port
    if ser.is_open:
        ser.close()
