import numpy as np

def normalize(v):
    return v / np.linalg.norm(v)

def calculate_final_rotation(rotation_vec, velocity_vec):
    # Convert rotation from degrees per second to radians per second
    rotation_vec_rad = np.radians(rotation_vec)
    
    # Normalizing the velocity vector to use as the new z-axis
    z_axis = normalize(velocity_vec)
    
    # Arbitrarily choosing the global y-axis to find a perpendicular x-axis
    if np.allclose(z_axis, [0, 1, 0]):
        # If the velocity vector is vertical, use global x-axis instead
        arbitrary_axis = np.array([1, 0, 0])
    else:
        arbitrary_axis = np.array([0, 1, 0])
    
    x_axis = normalize(np.cross(arbitrary_axis, z_axis))
    y_axis = np.cross(z_axis, x_axis)
    
    # Creating rotation matrix from the new basis vectors
    rotation_matrix = np.array([x_axis, y_axis, z_axis]).T
    
    # Transforming the rotation vector to the new coordinate system
    new_rotation_vec_rad = rotation_matrix @ rotation_vec_rad
    
    # Convert radians per second back to degrees per second
    new_rotation_vec_deg = np.degrees(new_rotation_vec_rad)
    
    # Convert from degrees per second to full rotations per second
    final_rotation_vec = new_rotation_vec_deg / 360.0
    
    return final_rotation_vec

# Example input
rotation_vector = np.array([-1307.14538574219,27410.15625,7050.71337890625])
velocity_vector = np.array([4.2130126953125,-1.48070847988129,-6.46631383895874])

# Calculate final rotation
final_rotation_vector = calculate_final_rotation(rotation_vector, velocity_vector)
print(final_rotation_vector)
