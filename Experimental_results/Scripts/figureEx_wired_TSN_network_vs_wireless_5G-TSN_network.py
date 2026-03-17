import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.ndimage import gaussian_filter1d

# --- Configuration ---
# Path to the Results folder inside ExpEx
results_dir = os.path.join('..', 'ExpEx', 'Results')

def load_npz_files(base_path):
    """Loads all .npz files containing the target result string from a directory."""
    data_list = []
    if not os.path.exists(base_path):
        print(f"Error: Directory not found -> {os.path.abspath(base_path)}")
        return data_list

    for root_dir, _, files in os.walk(base_path):
        for file in files:
            # Matches the format shown in your image
            if file.endswith('.npz') and 'RESULT_VECTOR_TAS_DL_DC' in file:
                full_path = os.path.join(root_dir, file)
                try:
                    npz_content = np.load(full_path, allow_pickle=True)
                    data_list.append((file, dict(npz_content)))
                except Exception as e:
                    print(f'Error loading {file}: {e}')
    return data_list

def compute_metrics(data):
    return {
        "min": np.nanmin(data),
        "max": np.nanmax(data),
        "mean": np.nanmean(data),
        "p999": np.nanpercentile(data, 99.9)
    }

def plot_pmf_with_profile(ax, data, bins, title, unit):
    # Data cleaning
    data = np.array(data).flatten()
    data = data[~np.isnan(data)]
    
    counts, bin_edges = np.histogram(data, bins=bins)
    probabilities = counts / np.sum(counts)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    width = bin_edges[1] - bin_edges[0]

    # PMF Bars
    ax.bar(bin_centers, probabilities, width=width*0.9, label="PMF", alpha=0.5, color='steelblue')

    # Smoothed Distribution Profile
    profile = gaussian_filter1d(probabilities, sigma=2)
    ax.plot(bin_centers, profile, color="red", linewidth=2, label="Distribution Profile")

    # Metrics
    metrics = compute_metrics(data)
    ax.axvline(metrics["min"], color='green', linestyle='--', label=f"Min: {metrics['min']:.2f}")
    ax.axvline(metrics["max"], color='black', linestyle='--', label=f"Max: {metrics['max']:.2f}")
    ax.axvline(metrics["p999"], color='purple', linestyle='-.', label=f"P99.9: {metrics['p999']:.2f}")
    ax.axvline(metrics["mean"], color='darkorange', linestyle=':', label=f"Mean: {metrics['mean']:.2f}")

    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(f"Port-to-Port Delay [{unit}]")
    ax.set_ylabel("Probability (PMF)")

    ax.xaxis.set_major_locator(MaxNLocator(10))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(which="major", linestyle="--", linewidth=0.6, alpha=0.6)
    ax.legend(loc="upper right", fontsize='small', frameon=True)

# --- Main Execution ---
results = load_npz_files(results_dir)

wired_us = None
wireless_ms = None

# Identify files based on the 'WIRED' or 'WIRELESS' suffix
for filename, content in results:
    if "WIRED" in filename.upper():
        wired_us = content['delays'] * 1000  # Convert to microseconds
    elif "WIRELESS" in filename.upper():
        wireless_ms = content['delays']      # Keep as milliseconds

# Validation
if wired_us is None or wireless_ms is None:
    print(f"Error: Could not find matching files in {results_dir}")
    print(f"Files found: {[f[0] for f in results]}")
    exit()

# --- Plotting ---
plt.rcParams.update({"axes.facecolor": "white", "figure.facecolor": "white"})
fig, axes = plt.subplots(2, 1, figsize=(8, 10))

plot_pmf_with_profile(axes[0], wired_us, bins=150, title="Wired TSN Bridge Latency", unit="µs")
plot_pmf_with_profile(axes[1], wireless_ms, bins=80, title="5G Wireless System Latency", unit="ms")

plt.tight_layout()
plt.show()