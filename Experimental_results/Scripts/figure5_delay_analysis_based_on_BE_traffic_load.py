import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Matplotlib configuration for LaTeX and font size
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 14})

# Directory path for experimental results
dir_path = '../Exp5/Results'
delay_data = []
file_names = []

# Predefined line styles for visibility
line_styles = [
    '-', '--', '-.', ':',
    (0, (3, 1, 1, 1)),
    (0, (4, 2)),
    (0, (2, 2)),
    (0, (5, 1, 1, 1)),
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (6, 2, 2, 2)),
    (0, (1, 1))
]

# Data loading
for root_dir, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_' in file:
            full_path = os.path.join(root_dir, file)
            try:
                npz_content = np.load(full_path, allow_pickle=True)
                if 'delays' in npz_content:
                    delay_data.append(npz_content['delays'])
                    clean_name = file.replace('.npz', '').replace('RESULT_VECTOR_TAS_DL_', '')
                    file_names.append(clean_name)
            except Exception as e:
                print(f'Error reading {file}: {e}')

# Create figure with two subplots (Broken Axis setup)
# Ratio 3:1 to highlight the initial delay distribution
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 6), 
                               gridspec_kw={'width_ratios': [3, 1]})

plotted_lines = []

for i, delays in enumerate(delay_data):
    if len(delays) == 0:
        continue
    
    # Calculate sorted data and CCDF
    sorted_delays = np.sort(delays)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)
    ccdf = 1 - cdf
    
    # Apply line style from the predefined list
    style = line_styles[i % len(line_styles)]
    
    line, = ax1.plot(sorted_delays, ccdf, linestyle=style)
    ax2.plot(sorted_delays, ccdf, linestyle=style)
    plotted_lines.append(line)

# Updated legend values for Best Effort generated traffic (Mbps)
legend_values = [600, 650, 700, 750, 800, 850, 950, 950, 980]

# Synchronize labels with the number of curves
num_lines = len(plotted_lines)
if num_lines != len(legend_values):
    print(f"Warning: {num_lines} curves found but {len(legend_values)} labels provided.")
    if num_lines < len(legend_values):
        legend_values = legend_values[:num_lines]
    else:
        legend_values += [legend_values[-1]] * (num_lines - len(legend_values))

# Generate labels with the new format
labels = [f"$R_{{BE}}^{{gen}}= {val}$ Mbps" for val in legend_values]

# Axis scaling and limits
ax1.set_xlim(3.5, 21)
ax2.set_xlim(45, 55)
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_ylabel('CCDF')

# Grid setup
ax1.grid(True, which='both', linestyle='--', alpha=0.6)
ax2.grid(True, which='both', linestyle='--', alpha=0.6)

# Hide inner spines for the "broken axis" visual effect
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax1.yaxis.tick_left()
ax2.yaxis.tick_right()

# Draw diagonal cut markers
d = .015
marker_kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (-d, +d), **marker_kwargs)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **marker_kwargs)
marker_kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, +d), (-d, +d), **marker_kwargs)
ax2.plot((-d, +d), (1 - d, 1 + d), **marker_kwargs)

# Global X-axis label
fig.text(0.5, 0.02, 'Packet Transmission Delay $\\widetilde{d}_{DC}^{emp}$ (ms)', 
         ha='center', fontsize=16)

# Place the legend in the first subplot (left) as per your request
ax1.legend(plotted_lines, labels, loc='lower left', fontsize=12, frameon=True, ncol=1)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()