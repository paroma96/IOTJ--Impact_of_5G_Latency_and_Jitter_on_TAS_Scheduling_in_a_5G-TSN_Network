import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import ConnectionPatch

# Matplotlib configuration for LaTeX rendering and font size
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 16})

# Path to the directory containing the experimental data
dir_path = '../Exp1'

# Lists to store the loaded data and corresponding filenames
delay_data = []
file_names = []

# Define line styles for the different plots to ensure visibility
line_styles = ['-', '--', '-.', ':', (0, (3,1,1,1)), (0, (5,5)), (0, (1,10))]

# Data loading loop: search for .npz files containing the target string
for root_dir, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_DC' in file:
            full_path = os.path.join(root_dir, file)
            try:
                npz_data = np.load(full_path, allow_pickle=True)
                if 'delays' in npz_data:
                    delay_data.append(npz_data['delays'])
                    file_names.append(file)
            except Exception as e:
                print(f'Error loading {file}: {e}')

# Custom LaTeX labels for the legend
custom_labels = [
    r'$W_{\mathrm{MS,DC}}=10.5\,\mu\mathrm{s}$',
    r'$W_{\mathrm{MS,DC}}=19.5\,\mu\mathrm{s}$',
    r'$W_{\mathrm{MS,DC}}=28.5\,\mu\mathrm{s}$',
    r'$W_{\mathrm{MS,DC}}=37.5\,\mu\mathrm{s}$',
    r'$W_{\mathrm{MS,DC}}=46.5\,\mu\mathrm{s}$',
]

# Create figure and main axes
fig, ax = plt.subplots(figsize=(6.5, 4.75))

# Plot the Cumulative Distribution Function (CDF) for each dataset
for i, delay in enumerate(delay_data):
    if len(delay) == 0:
        continue
    # Calculate sorted data and CDF values
    sorted_data = np.sort(delay)
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    
    style = line_styles[i % len(line_styles)]
    label = custom_labels[i] if i < len(custom_labels) else file_names[i]
    ax.plot(sorted_data, cdf, linestyle=style, label=label)

# Zoom (inset) limits
x1, x2 = 13, 17.45
y1, y2 = 0.9985, 1.000

# Inset position and size configuration
width = 0.6
height = 0.65
margin_right = 0.03
margin_bottom = 0.4

x_pos = 1 - width - margin_right
y_pos = (1 - height + margin_bottom) / 2
bbox_to_anchor = (x_pos, y_pos, width, height)

# Create the inset axes
axins = inset_axes(ax, width=f"{int(width*100)}%", height=f"{int(height*100)}%",
                   bbox_to_anchor=bbox_to_anchor,
                   bbox_transform=ax.transAxes,
                   loc='lower right',
                   borderpad=0)

# Plot the same data on the inset for the zoomed view
for i, delay in enumerate(delay_data):
    if len(delay) == 0:
        continue
    sorted_data = np.sort(delay)
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    style = line_styles[i % len(line_styles)]
    axins.plot(sorted_data, cdf, linestyle=style)

# Specific configuration for the inset axes (zoom area)
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.xaxis.set_major_locator(MultipleLocator(1))  # Ticks every 1ms
axins.grid(True, linestyle='--', alpha=0.6)

# Configuration for the main axes
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.set_xlim(4, 18.45)

# Drawing connection patches between the main plot and the inset
con1 = ConnectionPatch(xyA=(x1, y2), coordsA=ax.transData,
                       xyB=(x1, y2), coordsB=axins.transData,
                       color='0.5', linewidth=1)
con2 = ConnectionPatch(xyA=(x2, y2), coordsA=ax.transData,
                       xyB=(x2, y2), coordsB=axins.transData,
                       color='0.5', linewidth=1)
fig.add_artist(con1)
fig.add_artist(con2)

# Axis labels
ax.set_xlabel('Packet Transmission Delay $\\widetilde{d}_{DC}^{emp}$ (ms)')
ax.set_ylabel('CDF')

# Final plot adjustments and display
ax.legend(loc='lower right', fontsize=14, ncol=2)
ax.grid(True)
fig.subplots_adjust(left=0.12, right=0.98, bottom=0.17, top=0.97)
plt.show()