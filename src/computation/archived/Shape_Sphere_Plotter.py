import numpy as np
import matplotlib.pyplot as plt

# Need to end in .xyz
Input_File_Name = str(input("Name of input file: "))

# Plotting every Nth point to reduce computational time
Interval = int(input("Enter the interval: "))

def draw_unit_sphere(ax, resolution=50):
    """ 
    Draws a sphere based on the spherical coordinate system. 
    """
    
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    # The sphere is set to 10% opaque and 90% transparent
    ax.plot_surface(x, y, z, color='c', alpha=0.1, edgecolor='none')

def read_xyz_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def parse_xyz(file_content):
    lines = file_content.strip().split('\n')
    
    # We assume each "chunk" of data starts with "Point = 3"
    num_steps = len(lines) // 5
    
    x1 = np.zeros((num_steps, 3))
    x2 = np.zeros((num_steps, 3))
    x3 = np.zeros((num_steps, 3))
    
    for i in range(num_steps):
        base_index = i * 5 + 2
        
        x1_coords = lines[base_index].split()[1:4]  # Take only the first three coordinates
        x2_coords = lines[base_index + 1].split()[1:4]
        x3_coords = lines[base_index + 2].split()[1:4]
        
        x1[i] = np.array([float(coord) for coord in x1_coords])
        x2[i] = np.array([float(coord) for coord in x2_coords])
        x3[i] = np.array([float(coord) for coord in x3_coords])
    
    return x1, x2, x3, num_steps

# Read file content
file_content = read_xyz_file(Input_File_Name)

# Parse the file content
x1, x2, x3, num_steps = parse_xyz(file_content)


def to_shape_sphere(x1, x2, x3):
    """
    The details of the mapping can be seen here: https://henry-yip.github.io/ShapeSphere
    """
    
    # Convering to Jacobi Coordinates
    z1 = (x3 - x2) / np.sqrt(2)
    z2 = np.sqrt(2/3) * (x1 - (x2 + x3) / 2)
    
    # Applying the Hopf map
    u1 = np.linalg.norm(z1)**2 - np.linalg.norm(z2)**2
    u2 = 2 * (z1[0] * z2[0] + z1[1] * z2[1])
    u3 = 2 * (z1[0] * z2[1] - z1[1] * z2[0])
    
    # Normalizing the results
    norm_u = np.sqrt(u1**2 + u2**2 + u3**2)
    normalized_point = (u1/norm_u, u2/norm_u, u3/norm_u)
    return normalized_point

# Compute points on the shape sphere
points_on_sphere = []
for i in range(num_steps):
    if i % Interval == 0:
        point = to_shape_sphere(x1[i], x2[i], x3[i])
        points_on_sphere.append(point)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

points_on_sphere = np.array(points_on_sphere)
x_coords, y_coords, z_coords = points_on_sphere[:, 0], points_on_sphere[:, 1], points_on_sphere[:, 2]

# Plot the normalized points
ax.scatter(x_coords, y_coords, z_coords, label='Every {}th Point'.format(Interval))

# Draw the unit sphere
draw_unit_sphere(ax, 50)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set the aspect ratio to be equal
ax.set_box_aspect([1, 1, 1])  

# Connect the points with lines
ax.plot(x_coords, y_coords, z_coords)

# Show the plot
plt.show()