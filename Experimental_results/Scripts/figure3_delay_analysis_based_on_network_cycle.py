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

def load_npz_files(base_path):
    """Loads all .npz files containing the target result string from a directory."""
    data_list = []
    for root_dir, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_DC' in file:
                full_path = os.path.join(root_dir, file)
                try:
                    npz_content = np.load(full_path, allow_pickle=True)
                    data_list.append((file, dict(npz_content)))
                except Exception as e:
                    print(f'Error loading {file}: {e}')
    return data_list

# Configuration
results_dir = '../Exp3/Results'
results = load_npz_files(results_dir)

bin_width = 0.15
bins = np.arange(0, 31, bin_width)
bin_centers = bins[:-1]

# Custom LaTeX labels from the experiment
custom_labels = [
    r'$W_{\mathrm{MS,DC}}=9\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=6\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=12\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=8\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=15\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=10\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=18\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=12.5\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=22.5\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=15\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=25.5\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=17.5\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=30.0\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=20\,\mathrm{ms}$',
    r'$W_{\mathrm{MS,DC}}=33.0\,\mu\mathrm{s}, T_{\mathrm{MS}}^{\mathrm{NC}}=22.5\,\mathrm{ms}$',
]

# Filter indices to plot (excluding 6 and 7 as per original script)
indices_to_plot = [i for i in range(len(custom_labels)) if i not in [6, 7]]

# --- Robust parsing from custom_labels ---
def parse_T_ms(lbl):
    match = re.search(r'T_{\s*\\mathrm\{MS\}\s*}\^{\\mathrm\{NC\}}\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*(?=\\,|,)', lbl)
    return float(match.group(1)) if match else 0.0

def parse_W_us(lbl):
    match = re.search(r'W_{\s*\\mathrm\{MS,DC\}\s*}\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*(?=\\,|,|\\mu)', lbl)
    return float(match.group(1)) if match else 0.0

# --- Process series into a sorted list ---
data_series = []
for idx in indices_to_plot:
    fname, content = results[idx]
    delays = np.asarray(content['delays'], float)
    T_ms = parse_T_ms(custom_labels[idx])
    W_us = parse_W_us(custom_labels[idx])
    data_series.append((T_ms, W_us, custom_labels[idx], delays))

# Sort by Network Cycle (T) then by Window Size (W)
data_series.sort(key=lambda x: (x[0], x[1]))

# --- Format X-axis labels (Two lines: T top, W bottom) ---
def fmt_num(val):
    return f'{int(val)}' if abs(val - round(val)) < 1e-9 else f'{val:.1f}'

x_axis_labels = [
    rf'$\displaystyle T_{{\mathrm{{i}}}}^{{\mathrm{{nc}}}}={fmt_num(T)}\,\mathrm{{ms}}$' + '\n' +
    rf'$\displaystyle W_{{\mathrm{{i,DC}}}}={fmt_num(W)}\,\mu\mathrm{{s}}$'
    for (T, W, _, _) in data_series
]

# --- Extract peaks/windows from histogram ---
group_times, group_probs = [], []

for (_, _, _, d) in data_series:
    counts, _ = np.histogram(d, bins=bins)
    total = counts.sum()
    probs = counts / total if total > 0 else counts.astype(float)
    
    mask = probs > 0
    t_open = bin_centers[mask]
    p_open = probs[mask]

    # Compact contiguous segments and keep the peak of each segment
    if t_open.size > 1:
        keep_indices = []
        start_idx = 0
        for i in range(1, t_open.size + 1):
            if i == t_open.size or (t_open[i] - t_open[i-1]) > 1.5 * bin_width:
                segment = slice(start_idx, i)
                peak_idx = segment.start + int(np.argmax(p_open[segment]))
                keep_indices.append(peak_idx)
                start_idx = i
        t_open = t_open[keep_indices]
        p_open = p_open[keep_indices]

    sorted_idx = np.argsort(t_open)
    group_times.append(t_open[sorted_idx])
    group_probs.append(p_open[sorted_idx])

# --- Visual Setup ---
max_windows = max((len(t) for t in group_times), default=0)
color_palette = {1: "#004C99", 2: "#E66100"}  # Dark blue, Dark orange
standard_cmap = plt.get_cmap('tab10')
for j in range(3, max_windows + 1):
    color_palette[j] = standard_cmap((j - 1) % 10)

window_legend_names = {
    1: r'\textit{First Transmission Window}',
    2: r'\textit{Second Transmission Window}',
    3: r'\textit{Third Transmission Window}',
    4: r'\textit{Fourth Transmission Window}',
    5: r'\textit{Fifth Transmission Window}',
}

# ===== FIGURE: ORDERED OVERLAY WITH FLOATING PROBABILITY TEXT =====
fig, ax = plt.subplots(figsize=(12, 5.25))
x_positions = np.arange(len(data_series))

for i, (times, probs) in enumerate(zip(group_times, group_probs)):
    if times.size == 0:
        continue

    # 1) Draw bars in stack order (Window 3 back -> Window 1 front)
    draw_order = [3, 2, 1]
    for j in draw_order:
        if j <= len(times):
            delay_val = times[j - 1]
            z_val = {3: 1, 2: 2, 1: 3}.get(j, 1)

            ax.bar(
                x_positions[i],
                delay_val,
                width=0.6,
                color=color_palette.get(j),
                edgecolor='black',
                linewidth=1.0,
                zorder=z_val,
            )

    # 2) Annotate probabilities above the bars
    highest_y = np.max(times)
    y_text_start = highest_y + 1.0  # Offset above the highest bar
    vertical_step = 4.0             # Space between stacked text labels

    for k, p in enumerate(probs):
        ax.text(
            x_positions[i],
            y_text_start + k * vertical_step,
            rf'$\mathrm{{Prob.=}}\,{p:.4f}$',
            ha='center',
            va='bottom',
            fontsize=16,
            color=color_palette.get(k + 1, "black"),
            zorder=10,
        )

# --- Axes Configuration ---
ax.set_xticks(x_positions, x_axis_labels)
ax.set_xlabel(r'TAS Configuration')
ax.set_ylabel(r'Packet Transmission Delay $d_{DC}^{\mathrm{emp}}$ (ms)')

ax.set_ylim(0, 55.0)
ax.set_yticks(np.arange(0, 55.1, 5.0))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: rf'${int(v)}$'))

ax.grid(True, axis='y', linestyle='--', linewidth=0.5, zorder=0)
ax.margins(x=0.04)

# --- Legend ---
legend_elements = [
    Patch(
        facecolor=color_palette[j],
        edgecolor='black',
        label=window_legend_names.get(j, rf'\textit{{Transmission Window {j}}}')
    )
    for j in range(1, max_windows + 1)
]

if legend_elements:
    leg = ax.legend(
        handles=legend_elements,
        title=r'\textbf{\shortstack[l]{Network cycle in which\\a packet is transmitted from SL}}',
        loc='upper right',
        frameon=True,
        ncol=1,
        handletextpad=0.4
    )
    leg._legend_box.align = "left"

fig.tight_layout()
plt.show()