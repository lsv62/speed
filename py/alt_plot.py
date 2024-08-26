import matplotlib.pyplot as plt
import numpy as np

def calculate_altitude(pressure, ground_level_pressure=1.01325):
    # Constants
    L = 0.0065  # Temperature lapse rate (K/m)
    T0 = 288.15  # Standard temperature at sea level (K)
    g = 9.80665  # Acceleration due to gravity (m/s^2)
    M = 0.0289644  # Molar mass of Earth's air (kg/mol)
    R = 8.31447  # Universal gas constant (J/(mol·K))
    
    # Calculate altitude using barometric formula
    altitude = (T0 / L) * (1 - (pressure / ground_level_pressure)**((R * L) / (g * M))) / 1000.0  # Convert to kilometers
    
    return altitude

def calculate_pressure(altitude,ground_level_pressure=1.01325):
    # Constants
    L = 0.0065  # Temperature lapse rate (K/m)
    T0 = 288.15  # Standard temperature at sea level (K)
    g = 9.80665  # Acceleration due to gravity (m/s^2)
    M = 0.0289644  # Molar mass of Earth's air (kg/mol)
    R = 8.31447  # Universal gas constant (J/(mol·K))
    
    # Calculate pressure using barometric formula
    pressure = ground_level_pressure*(1 - (altitude*1000.0*L/T0))**((g * M)/(R * L))   # Convert to kilometers
    
    return pressure 

alts = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0]
measures = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.01, 5.01, 6.02, 7.03]

# Convert lists to numpy arrays
alts_array = np.array(alts)
pressure_array = np.array(measures)
measure_array = np.array(measures)
mp3_array = np.array(measures)
mm3_array = np.array(measures)
i=0
for alt in alts_array:
    pressure_array[i] = calculate_pressure(alt)
    mp3_array[i]= pressure_array[i]*1.03
    measure_array[i]=calculate_altitude(pressure_array[i])-calculate_altitude(mp3_array[i])
    i=i+1

# Create the plot
plt.figure(figsize=(10, 6))  # Optional: set the figure size
plt.plot(alts, measure_array, marker='o', linestyle='-', color='b', label='alt errors')
# Add titles and labels
plt.title('Pressure measurements with error of 3 persent')
plt.xlabel('Altitude, km')
plt.ylabel('Altitude error, km')

# Add a legend (optional)
plt.legend()

# Display the plot
plt.show()
