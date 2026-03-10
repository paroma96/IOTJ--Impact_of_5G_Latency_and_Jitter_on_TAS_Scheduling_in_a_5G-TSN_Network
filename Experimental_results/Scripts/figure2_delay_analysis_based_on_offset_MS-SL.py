import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

# Matplotlib configuration for LaTeX and font size
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 16})

# Directory path and initialization
dir_path = '../Exp2/Results'
delays_per_file = {}

# Load experimental data (.npz files)
for file_name in os.listdir(dir_path):
    if file_name.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_DC' in file_name:
        full_path = os.path.join(dir_path, file_name)
        with np.load(full_path) as data:
            if 'delay' in data or 'delays' in data:
                key = 'delay' if 'delay' in data else 'delays'
                delays_per_file[file_name] = data[key]

# Labels for the different experimental configurations
exp_labels = [
    r'$\delta_{DC}=10\,\mathrm{ms}$',
    r'$\delta_{DC}=15\,\mathrm{ms}$',
    r'$\delta_{DC}=20\,\mathrm{ms}$',
    r'$\delta_{DC}=25\,\mathrm{ms}$',
    r'$\delta_{DC}=30\,\mathrm{ms}$',
    r'$\delta_{DC}=5\,\mathrm{ms}$'
]

def delta_from_label(lbl):
    """Extracts the numerical delta value from the LaTeX label string."""
    match = re.search(r'=\s*(\d+(?:\.\d+)?)\\,\\mathrm\{ms\}', lbl)
    if not match:
        raise ValueError(f"Cannot parse delta from label: {lbl}")
    return float(match.group(1))

# --- Data Processing: Load, Pair, and Sort ---
series_delays = [delays for _, delays in delays_per_file.items()]
deltas_ms_raw = [delta_from_label(s) for s in exp_labels]
min_len = min(len(series_delays), len(deltas_ms_raw))
data_pairs = [(deltas_ms_raw[i], np.asarray(series_delays[i], float)) for i in range(min_len)]
data_pairs.sort(key=lambda x: x[0])

sorted_delta = [p[0] for p in data_pairs]
sorted_delays = [p[1] for p in data_pairs]
x_axis_labels = [rf'$\delta_{{DC}}={d:.0f}\,\mathrm{{ms}}$' for d in sorted_delta]

# --- Probability Calculation per Transmission Window ---
ticks_per_delta, probs_per_delta, counts_per_delta = [], [], []
offset_correction = 0.025 # Shift to avoid splitting data at the exact window edge

for delays, delta_ms in zip(sorted_delays, sorted_delta):
    d_adj = np.asarray(delays, float) - offset_correction 
    d_adj = np.maximum(d_adj, 0.0) 
    
    # Calculate window index (k) for each sample
    k_indices = np.floor(d_adj / delta_ms).astype(int) + 1
    k_indices = k_indices[k_indices > 0]
    
    if k_indices.size == 0:
        ticks_per_delta.append(np.array([], float))
        probs_per_delta.append(np.array([], float))
        counts_per_delta.append(0)
        continue
        
    unique_k = np.unique(k_indices)
    ticks = unique_k * delta_ms
    probabilities = [np.mean((d_adj >= (kv - 1) * delta_ms) & (d_adj < kv * delta_ms)) for kv in unique_k]
    
    ticks_per_delta.append(ticks)
    probs_per_delta.append(np.asarray(probabilities))
    counts_per_delta.append(len(unique_k))

# --- Visual Configuration (Colors and Names) ---
max_windows = max(counts_per_delta) if counts_per_delta else 0
cmap = plt.get_cmap('tab10')
local_colors = {1: "#004C99", 2: "#E66100"} # Default palette
for j in range(3, max_windows + 1):
    local_colors[j] = cmap((j - 1) % 10)

window_names = {
    1: r'\textit{First Transmission Window}',
    2: r'\textit{Second Transmission Window}',
    3: r'\textit{Third Transmission Window}',
    4: r'\textit{Fourth Transmission Window}',
    5: r'\textit{Fifth Transmission Window}',
}

# ===== FIGURE: OVERLAID BARS =====
fig, ax = plt.subplots(figsize=(11, 5))
x_pos = np.arange(len(x_axis_labels))

for i, (ticks, probs) in enumerate(zip(ticks_per_delta, probs_per_delta)):
    if ticks.size == 0:
        continue

    # Draw order to handle z-stacking (Window 3 back, Window 1 front)
    draw_order = [3, 2, 1]

    for j in draw_order:
        if j <= len(ticks):
            tk = ticks[j - 1]
            z_idx = {3: 1, 2: 2, 1: 3}.get(j, 1)

            ax.bar(
                x_pos[i],
                tk,
                width=0.6,
                color=local_colors.get(j, cmap((j - 1) % 10)),
                edgecolor='black',
                linewidth=1.0,
                zorder=z_idx,
            )

    # Place probability annotations above the bars
    y_max = np.max(ticks)
    text_y_base = y_max + 1.0
    v_spacing = 4.0

    for k, p in enumerate(probs):
        ax.text(
            x_pos[i],
            text_y_base + k * v_spacing,
            rf'$\mathrm{{Prob.=}}\,{p:.4f}$',
            ha='center',
            va='bottom',
            fontsize=16,
            color=local_colors.get(k + 1, "black"),
            zorder=10,
        )

# --- Axes and Grid Formatting ---
ax.set_xticks(x_pos, x_axis_labels)
ax.set_xlabel(r'TAS offset')
ax.set_ylabel(r'Packet Transmission Delay $d_{DC}^{\mathrm{emp}}$ (ms)')

ax.set_ylim(0, 55.0)
ax.set_yticks(np.arange(0, 55.1, 5.0))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: rf'${int(v)}$'))
ax.grid(True, axis='y', linestyle='--', linewidth=0.5, zorder=0)
ax.margins(x=0.04)

# --- Legend Configuration ---
legend_patches = [
    Patch(facecolor=local_colors[j], edgecolor='black',
          label=window_names.get(j, rf'\textit{{Transmission Window {j}}}'))
    for j in range(1, max_windows + 1)
]

if legend_patches:
    leg = ax.legend(
        handles=legend_patches,
        title=r'\textbf{\shortstack[l]{Network cycle in which\\a packet is transmitted from SL}}',
        loc='upper right',
        frameon=True,
    )
    leg._legend_box.align = "left"

fig.tight_layout()
plt.show()