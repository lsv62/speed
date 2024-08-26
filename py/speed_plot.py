import matplotlib.pyplot as plt
import numpy as np

speed = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
measure = [0, 21.67, 41.31, 61.5, 81.87, 102.6, 123.6, 144.9, 166.58, 188.7, 211.2]

# Convert lists to numpy arrays
speed_array = np.array(speed)
measure_array = np.array(measure)

# Subtract element-wise
result = measure_array - speed_array

# Create the plot
plt.figure(figsize=(10, 6))  # Optional: set the figure size
plt.plot(speed, result, marker='o', linestyle='-', color='b', label='Errors')

# Add titles and labels
plt.title('Speed measurements')
plt.xlabel('Speed, m/s')
plt.ylabel('Speed error, m/s')

# Add a legend (optional)
plt.legend()

# Display the plot
plt.show()
