import matplotlib.pyplot as plt

# Sample data
x = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.00, 5.00, 6.00, 7.00]
y = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.01, 5.01, 6.02, 7.03]

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
ax.set_xlabel('Задана висота, км')
ax.set_ylabel('Похибка вимірювання, км')
ax.set_title('Похибка барометричного висотоміра')

# Save the figure
plt.savefig('_static/alt.png')
