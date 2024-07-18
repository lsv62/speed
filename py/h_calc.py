L = 0.0065  # Temperature lapse rate (K/m)
T0 = 288.15  # Standard temperature at sea level (K)
g = 9.80665  # Acceleration due to gravity (m/s^2)
M = 0.0289644  # Molar mass of Earth's air (kg/mol)
R = 8.31447  # Universal gas constant (J/(mol·K))

# Calculate altitude using barometric formula
exponent = (R * L) / (g * M)
base = 1 - (1.0123 / 1.0241
altitude = ((T0 / L) * (1 - (1.0123 / 1.0241)**(exponent))) / 1000.0  # Convert to kilometers

print("Altitude: {:.2f} km".format(altitude))
print("Exponent: {:.4f}".format(exponent))
print("multiply: {:2.4f}".format((T0 / L) / 1000.))
print("base: {:1.6f}".format(1 - (1.0123 / 1.0241)))