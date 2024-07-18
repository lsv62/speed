import matplotlib.pyplot as plt

# Sample data
x = [0, 20, 40, 60, 80, 100,120,140,160,180,200]
y = [0, 21.67, 41.31, 61.5,  81.87, 102.6, 123.6, 144.9, 166.58,188.7, 211.2]

# Calculate differences using list comprehension
z = [y[i] - x[i] for i in range(len(x))]

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, z, label='Column 1')

# Customize grid appearance
plt.grid(True)  # Enable grid
plt.grid(which='both', axis='both', linestyle='--', linewidth=0.5)  # Customize grid lines

# Add labels and title
ax.set_xlabel('Задана швидкість, м/с')
ax.set_ylabel('Похибка вимірювання, м/с')
ax.set_title('Похибка вимірювання повітряної швидкості')

# Save the figure
plt.savefig('_static/speed.png')
