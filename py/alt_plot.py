import matplotlib.pyplot as plt
import numpy as np

alts = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0]
measures = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.01, 5.01, 6.02, 7.03]

# Convert lists to numpy arrays
alts_array = np.array(alts)
errors_array = np.array(measures)

# Subtract element-wise
result = errors_array - alts_array

# Create the plot
plt.figure(figsize=(10, 6))  # Optional: set the figure size
plt.plot(alts, result, marker='o', linestyle='-', color='b', label='Errors')

# Add titles and labels
plt.title('Altitude measurements')
plt.xlabel('Altitude, km')
plt.ylabel('Altitude error, km')

# Add a legend (optional)
plt.legend()

# Display the plot
plt.show()
