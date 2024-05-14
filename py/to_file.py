import datetime

# File path where you want to save the pressure data
file_path = 'data.txt'

# Open file for writing
with open(file_path, 'a') as file:

    # Write each pressure reading with timestamp to the file
    abs_pressure = 101325
    IAS = -15
    CAS = 0
    timestamp = datetime.datetime.now().isoformat()
    file.write(f'{timestamp} Pressure={abs_pressure}(Pa)')
    file.write(f' IAS={IAS}(m/s) CAS= {CAS}(m/s)\n')
    # Write timestamp and pressure value
