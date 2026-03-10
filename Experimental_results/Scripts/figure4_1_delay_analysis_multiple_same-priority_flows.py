import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# Matplotlib configuration for LaTeX rendering and font size
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 16})

# Directory path for the experimental results
dir_path = '../Exp4_1/Results'
delay_data = []
file_names = []

# Line styles: diverse and visible patterns for multiple curves
line_styles = [
    '-', '--', '-.', ':',
    (0, (3,1,1,1)), (0, (5,5)), (0, (1,10)),
    (0, (7,2,1,2)), (0, (3,5,1,5,1,5))
]

# Special style reserved for the last curve in the dataset
last_curve_style = (0, (5, 1))  # Long and short dashes

# Data loading loop: searching for .npz files with the target prefix
for root_dir, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_' in file:
            full_path = os.path.join(root_dir, file)
            print(f'Loading file: {full_path}')
            try:
                npz_content = np.load(full_path, allow_pickle=True)
                if 'delays' in npz_content:
                    delay_data.append(npz_content['delays'])
                    # Clean filename for fallback labeling
                    clean_name = file.replace('.npz', '').replace('RESULT_VECTOR_TAS_DL_', '')
                    file_names.append(clean_name)
                else:
                    print(f'File {file} does not contain "delays" field.')
            except Exception as e:
                print(f'Error loading {file}: {e}')

# X-axis values for the legend labels (Window sizes in ms)
w_values = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75]

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the Cumulative Distribution Function (CDF) for each dataset
for i, delay in enumerate(delay_data):
    if len(delay) == 0:
        print(f'File {file_names[i]} has empty delay data')
        continue

    # Sort data and calculate CDF values
    sorted_data = np.sort(delay)
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)

    # Assign line style: specific for the last one, cycled for others
    if i == len(delay_data) - 1:
        style = last_curve_style
    else:
        style = line_styles[i % len(line_styles)]

    # Generate legend label based on provided W values
    if i < len(w_values):
        label = rf'$W_{{\mathrm{{MS,DC}}}} = {w_values[i]:.2f}\,\mathrm{{ms}}$'
    else:
        label = file_names[i]

    ax.plot(sorted_data, cdf, linestyle=style, label=label)

# Main axes configuration
ax.set_xlabel('Packet Transmission Delay $\\widetilde{d}_{DC}^{emp}$ (ms)')
ax.set_ylabel('CDF')
ax.set_xlim(4, 23)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_ylim(0, 1.01)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

# Legend and grid setup
ax.legend(loc='lower right', fontsize=14, ncol=1)
ax.grid(True, which='both', linestyle='--', alpha=0.6)

# Zoom inset parameters
x1, x2 = 16, 23
y1, y2 = 0.9985, 1.0000

# Formatter function for 4 decimal places in the inset Y-axis
def format_4_decimals(x, pos):
    return f'{x:.4f}'

# Create a small inset at the upper left corner
ax_ins = inset_axes(ax, width="30%", height="40%", loc='upper left', borderpad=1)

# Re-plot the data inside the inset axes
for i, delay in enumerate(delay_data):
    if len(delay) == 0:
        continue
    sorted_data = np.sort(delay)
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    
    if i == len(delay_data) - 1:
        style = last_curve_style
    else:
        style = line_styles[i % len(line_styles)]
    ax_ins.plot(sorted_data, cdf, linestyle=style)

# Inset axes configuration (Zoom area)
ax_ins.set_xlim(x1, x2)
ax_ins.set_ylim(y1, y2)
ax_ins.grid(True, linestyle='--', alpha=0.6)

# Inset X-axis: Ticks every 1ms between 16 and 23
ax_ins.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax_ins.xaxis.set_ticks(np.arange(16, 24, 1))

# Inset Y-axis formatting: 4 decimals and labels moved to the right side
ax_ins.yaxis.set_major_formatter(FuncFormatter(format_4_decimals))
ax_ins.yaxis.set_label_position("right")
ax_ins.yaxis.tick_right()

# Draw the lines connecting the main plot with the zoom area
mark_inset(ax, ax_ins, loc1=2, loc2=4, fc="none", ec="0.5")

plt.tight_layout()
plt.show()