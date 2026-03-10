import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# Matplotlib configuration for LaTeX and font size
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 14})

# Directory path for experimental results
dir_path = '../Exp4_2/Results'
delay_data = []
file_names = []

# Predefined line styles for distinguishing multiple curves
line_styles = [
    '-', '--', '-.', ':',
    (0, (3,1,1,1)),
    (0, (5,5)),
    (0, (1,10)),
    (0, (7,2,1,2)),
    (0, (3,5,1,5,1,5))
]
last_curve_style = (0, (5, 1))  # Special style for the final dataset

# Data loading loop
for root_dir, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_' in file:
            full_path = os.path.join(root_dir, file)
            try:
                npz_content = np.load(full_path, allow_pickle=True)
                if 'delays' in npz_content:
                    delay_data.append(npz_content['delays'])
                    # Clean filename for internal reference
                    clean_name = file.replace('.npz', '').replace('RESULT_VECTOR_TAS_DL_', '')
                    file_names.append(clean_name)
            except Exception as e:
                print(f'Error reading {file}: {e}')

# Create figure with two subplots (broken axes effect)
# Ratio 3:1 to emphasize the first delay region
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12,6), gridspec_kw={'width_ratios': [3, 1]})

plotted_lines = []

# Main plotting loop for both subplots
for i, delays in enumerate(delay_data):
    if len(delays) == 0:
        continue
    
    # Calculate sorted data and CCDF (1 - CDF)
    sorted_delays = np.sort(delays)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)
    ccdf = 1 - cdf
    
    # Apply special style to the last curve, cycle styles for others
    style = last_curve_style if i == len(delay_data) - 1 else line_styles[i % len(line_styles)]
    
    line, = ax1.plot(sorted_delays, ccdf, linestyle=style)
    ax2.plot(sorted_delays, ccdf, linestyle=style)
    plotted_lines.append(line)

# Values for the legend labels (Window sizes in ms)
legend_values = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75]

# Sync legend values with the number of plotted lines
num_lines = len(plotted_lines)
if num_lines != len(legend_values):
    print(f"Warning: Found {num_lines} curves but {len(legend_values)} legend values.")
    if num_lines < len(legend_values):
        legend_values = legend_values[:num_lines]
    else:
        legend_values += [legend_values[-1]] * (num_lines - len(legend_values))

# Generate legend labels
labels = [f"$W_{{i,DC}}= {val:.2f}$ ms" for val in legend_values]

# Axis range and scale configuration
ax1.set_xlim(18, 21.6)
ax2.set_xlim(48, 51)
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_ylabel('CCDF')

# Grid configuration
ax1.grid(True, which='both', linestyle='--', alpha=0.6)
ax2.grid(True, which='both', linestyle='--', alpha=0.6)

# Hide inner spines to create the "broken axis" look
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax1.yaxis.tick_left()
ax2.yaxis.tick_right()

# Draw diagonal "broken axis" markers
d = .015
marker_kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (-d, +d), **marker_kwargs)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **marker_kwargs)
marker_kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, +d), (-d, +d), **marker_kwargs)
ax2.plot((-d, +d), (1 - d, 1 + d), **marker_kwargs)

# Common X-axis label centered at the bottom
fig.text(0.5, 0.02, 'Packet Transmission Delay $d_{DC}^{emp}$ (ms)', ha='center', fontsize=16)

# Legend placed in the second subplot (right)
ax2.legend(plotted_lines, labels, loc='upper right', fontsize=12, frameon=True)

# === ZOOM INSET ===
# Positioned relative to ax1
ax_ins = inset_axes(ax1,
                    width="80%", height="95%",
                    bbox_to_anchor=(0.05, 0.10, 0.5, 0.5),
                    bbox_transform=ax1.transAxes,
                    loc='lower left', borderpad=0)

# Re-plot data within the inset
for i, delays in enumerate(delay_data):
    if len(delays) == 0:
        continue
    sorted_delays = np.sort(delays)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)
    ccdf = 1 - cdf
    style = last_curve_style if i == len(delay_data) - 1 else line_styles[i % len(line_styles)]
    ax_ins.plot(sorted_delays, ccdf, linestyle=style)

# Inset axes configuration (zooming in on the 20ms transition)
ax_ins.set_xlim(19.95, 20.05)
ax_ins.set_ylim(ax1.get_ylim())
ax_ins.set_yscale('log')
ax_ins.grid(True, which='both', linestyle='--', alpha=0.6)
ax_ins.yaxis.set_ticks_position('right')
ax_ins.yaxis.set_label_position('right')

# Connection lines between the main plot and the inset
mark_inset(ax1, ax_ins, loc1=2, loc2=4, fc="none", ec="0.5")

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()