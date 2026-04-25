import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ------------------------------------------------------
# 1. Define the original shape: The letter "F" (asymmetric for clear visualization)
# ------------------------------------------------------
# Each column is a point [x; y]. We close the shape by repeating the first point at the end.
original_shape = np.array([
    [0, 0, 1, 1, 0.5, 0.5, 0.7, 0.7, 0.5, 0.5, 1, 1, 0, 0],  # X coordinates
    [0, 2, 2, 1.6, 1.6, 1.2, 1.2, 0.8, 0.8, 0.4, 0.4, 0, 0, 0]   # Y coordinates
])

# ------------------------------------------------------
# 2. Setup the plot layout
# ------------------------------------------------------
fig = plt.figure(figsize=(10, 10))
# Main plot area (leave space at bottom for sliders)
ax_main = fig.add_subplot(111)
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initialize plots
# Original shape (static blue)
line_orig, = ax_main.plot(original_shape[0, :], original_shape[1, :], 
                           color='#1f77b4', linewidth=3, label='Original Shape')
ax_main.fill(original_shape[0, :], original_shape[1, :], 
             color='#aec7e8', alpha=0.3)

# Transformed shape (dynamic red)
transformed_shape = original_shape.copy()
line_trans, = ax_main.plot(transformed_shape[0, :], transformed_shape[1, :], 
                            color='#ff7f0e', linewidth=3, label='Transformed Shape')
fill_trans = ax_main.fill(transformed_shape[0, :], transformed_shape[1, :], 
                           color='#ffbb78', alpha=0.5)[0]

# Configure main plot aesthetics
ax_main.set_xlim(-4, 4)
ax_main.set_ylim(-4, 4)
ax_main.axhline(y=0, color='black', linewidth=1, linestyle='--')
ax_main.axvline(x=0, color='black', linewidth=1, linestyle='--')
ax_main.grid(True, linestyle=':', alpha=0.6)
ax_main.set_aspect('equal', adjustable='box')
ax_main.set_title('Interactive Matrix Transformation Visualizer', fontsize=16, fontweight='bold')
ax_main.set_xlabel('X-axis', fontsize=12)
ax_main.set_ylabel('Y-axis', fontsize=12)
ax_main.legend(loc='upper right', fontsize=12)

# ------------------------------------------------------
# 3. Create Sliders for interactive parameters
# ------------------------------------------------------
# Define slider axes positions [left, bottom, width, height]
ax_rot = plt.axes([0.2, 0.25, 0.6, 0.03])
ax_scale_x = plt.axes([0.2, 0.20, 0.6, 0.03])
ax_scale_y = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_shear_x = plt.axes([0.2, 0.10, 0.6, 0.03])
ax_shear_y = plt.axes([0.2, 0.05, 0.6, 0.03])

# Create sliders
s_rot = Slider(ax_rot, 'Rotation (°)', -180, 180, valinit=0, valstep=1)
s_scale_x = Slider(ax_scale_x, 'Scale X', -3, 3, valinit=1, valstep=0.1)
s_scale_y = Slider(ax_scale_y, 'Scale Y', -3, 3, valinit=1, valstep=0.1)
s_shear_x = Slider(ax_shear_x, 'Shear X', -2, 2, valinit=0, valstep=0.1)
s_shear_y = Slider(ax_shear_y, 'Shear Y', -2, 2, valinit=0, valstep=0.1)

# ------------------------------------------------------
# 4. Update function (called when sliders change)
# ------------------------------------------------------
def update(val):
    # Get current slider values
    theta = np.radians(s_rot.val)  # Convert degrees to radians
    sx = s_scale_x.val
    sy = s_scale_y.val
    kx = s_shear_x.val
    ky = s_shear_y.val

    # 1. Rotation Matrix
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    # 2. Scaling Matrix
    S = np.array([
        [sx, 0],
        [0, sy]
    ])

    # 3. Shearing Matrix
    Sh = np.array([
        [1, kx],
        [ky, 1]
    ])

    # Combined Transformation Matrix: M = R * S * Sh (Order matters!)
    M = R @ S @ Sh

    # Apply transformation
    new_points = M @ original_shape

    # Update the plot data
    line_trans.set_data(new_points[0, :], new_points[1, :])
    fill_trans.set_xy(new_points.T)
    
    # Redraw the canvas
    fig.canvas.draw_idle()

# ------------------------------------------------------
# 5. Link sliders to update function
# ------------------------------------------------------
s_rot.on_changed(update)
s_scale_x.on_changed(update)
s_scale_y.on_changed(update)
s_shear_x.on_changed(update)
s_shear_y.on_changed(update)

# Show the interactive plot
print("Visualizer is ready! Drag the sliders to see real-time transformations.")
plt.show()
