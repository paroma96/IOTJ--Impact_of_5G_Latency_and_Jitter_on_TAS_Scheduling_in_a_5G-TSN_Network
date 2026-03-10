import os
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# === Global Configuration Parameters ===
LOG_SCALE = 0
PDF = 0
CCDF = 0
STEP = 900
MIN_OUTLAYER = 0
MAX_OUTLAYER = 1000

def read_csv(file_path):
    """Read the CSV file and return a list of tuples (seconds, nanoseconds, sequence), skipping the first 2 header rows."""
    data = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Skip first header row
            next(csv_reader, None)  # Skip second header row
            for row in csv_reader:
                if len(row) >= 3:  # Ensure row has enough columns
                    seconds = int(row[0])
                    nanoseconds = int(row[1])
                    sequence = int(row[2])
                    data.append((seconds, nanoseconds, sequence))
                else:
                    print(f"Invalid row in {file_path}: {row}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return data

def convert_to_milliseconds(seconds, nanoseconds):
    """Convert seconds and nanoseconds to a timestamp in milliseconds."""
    milliseconds = seconds * 1e3 + nanoseconds / 1e6
    return milliseconds

def calculate_delays(file1_data, file2_data):
    """Calculate delays between matching sequences in two files."""
    delays_ms = []
    file2_dict = {seq[2]: (seq[0], seq[1]) for seq in file2_data}
    common_seqs = set(seq[2] for seq in file1_data) & set(file2_dict.keys())
    if not common_seqs:
        print("No matching sequences found.")
        return delays_ms
    for seq1 in file1_data:
        if seq1[2] in file2_dict:
            seq2 = file2_dict[seq1[2]]
            timestamp1_ms = convert_to_milliseconds(seq1[0], seq1[1])
            timestamp2_ms = convert_to_milliseconds(seq2[0], seq2[1])
            delay_ms = timestamp2_ms - timestamp1_ms
            delays_ms.append(delay_ms)
    #print(delays_ms)
    return delays_ms

def min_max_latencies(lat_list):
    """
    Filter out latency values outside of defined bounds.
    """
    return [x for x in lat_list if MIN_OUTLAYER <= x <= MAX_OUTLAYER]

def plot_one_minus_cdf_log(delays_ms, label, marker):
    """
    Plot the 1-CDF (CCDF) or CDF of the delay values.
    """
    sorted_delays = np.sort(delays_ms)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)
    one_minus_cdf = 1 - cdf if CCDF else cdf

    x_markers = sorted_delays[::STEP]
    x_markers = np.concatenate(([sorted_delays[0]], x_markers))
    y_markers = one_minus_cdf[::STEP]
    y_markers = np.concatenate(([one_minus_cdf[0]], y_markers))

    plt.plot(sorted_delays, one_minus_cdf, linestyle='-', linewidth=2)
    plt.scatter(x_markers, y_markers, marker=marker, label=label)

def plot_pdf(delays_ms, label, marker):
    """
    Plot the Probability Density Function (PDF) of the delay values,
    similar in interface and behavior to plot_one_minus_cdf_log().
    """
    # Remove NaNs and ensure there are valid values
    delays_ms = np.array(delays_ms)
    delays_ms = delays_ms[~np.isnan(delays_ms)]
    if len(delays_ms) == 0:
        print(f"Warning: empty data for {label}")
        return

    # Compute histogram with normalization (area under curve = 1)
    density, bin_edges = np.histogram(delays_ms, bins=100, density=True)

    # Compute bin centers
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Explicitly normalize the area to 1 for consistency
    area = np.trapz(density, bin_centers)
    if area > 0:
        density /= area

    # Plot PDF curve
    plt.plot(bin_centers, density, linestyle='-', linewidth=2)

    # Add spaced markers for visibility
    step = max(1, len(bin_centers) // 15)
    plt.scatter(bin_centers[::step], density[::step], marker=marker, label=label)


def parse_value_with_unit(value, unit):
    """
    Convert a value with unit to milliseconds.
    """
    value = float(value)

    if unit == "us":
        return value / 1000.0
    elif unit == "ms":
        return value
    elif unit == "s":
        return value * 1000.0
    else:
        raise ValueError(f"Unknown unit: {unit}")


def format_value(value):
    """
    Format a value intelligently: use μs for values < 1ms, ms otherwise.

    Returns:
        (formatted_str, unit)
    """
    if value < 1.0:
        return f"{value * 1000:.1f} $\\mu$s"
    else:
        return f"{value:.2f} ms"


def extract_label_from_filename(file_name, experiment):
    """
    Extract and format the label based on the experiment type and file name.
    Applies unit formatting and removes negative signs.
    """

    # Extract numbers with units (e.g., 10.5us, 30ms)
    matches = re.findall(r'([0-9]*\.?[0-9]+)(us|ms|s)', file_name)

    # Convert everything to milliseconds internally
    values = [parse_value_with_unit(v, u) for v, u in matches]

    print(values)

    global LOG_SCALE, CCDF, PDF

    if experiment == "Exp1":
        LOG_SCALE = 0
        CCDF = 0
        w = values[0]
        w_str = format_value(w)
        return r"$W_{MS,DC}$ = " + w_str

    elif experiment == "Exp2":
        LOG_SCALE = 1
        CCDF = 1
        delta = values[-1]
        delta_str = format_value(delta)
        return r"$\delta_{DC}$ = " + delta_str

    elif experiment == "Exp3":
        LOG_SCALE = 1
        CCDF = 1
        w = values[0]
        T = values[1]
        w_str = format_value(w)
        T_str = format_value(T)
        return r"$W_{i,DC}$ = " + w_str + ", " + r"$T_{MS}^{nc}$ = " + T_str

    elif experiment in ["Exp4_1", "Exp4_2"]:
        if experiment in "Exp4_1":
            LOG_SCALE = 0
            CCDF = 0
        else:
            LOG_SCALE = 1
            CCDF = 1
        w = values[0]
        w_str = format_value(w)
        return r"$W_{MS,DC}$ = " + w_str

    elif experiment == "Exp5":
        LOG_SCALE = 1
        CCDF = 1
        R = int(re.search(r'R=(\d+)', file_name).group(1))
        return r"$R^{gen}_{BE}$ = " + f"{R} Mbps"
    
    elif experiment == "ExpEx":
        LOG_SCALE = 0
        #PDF = 1
        CCDF = 0
        return "Params: " + ", ".join(format_value(v) for v in values)

    else:
        # Fallback for unknown experiments
        return "Params: " + ", ".join(format_value(v) for v in values)


def process_npz_files(directory):
    """
    Load and plot all .npz result files from the 'Results' subdirectory.
    Constructs intelligent labels depending on the experiment type.
    """
    results_path = os.path.join(directory, "Results")
    files = sorted([f for f in os.listdir(results_path) if f.endswith(".npz")])
    experiment = os.path.basename(os.path.normpath(directory))

    markers = ["X", "v", "8", "D", "^", "*", "s", "<", "4", "H", "o", ">"]

    for i, file in enumerate(files):
        file_path = os.path.join(results_path, file)
        data = np.load(file_path, allow_pickle=True)
        delays_ms = data['delays']
        delays_ms = min_max_latencies(delays_ms)

        label = extract_label_from_filename(file, experiment)
        print(f"{file}: {len(delays_ms)} samples (min. latency: {min(delays_ms)} ms, max. latency: {max(delays_ms)} ms) -> {label}")

        if PDF:
            plot_pdf(delays_ms, label, markers[i % len(markers)])
        else:
            plot_one_minus_cdf_log(delays_ms, label, markers[i % len(markers)])


def process_pair(identifier, paths, marker, directory):
    """Process a single master-slave file pair."""
    master_path = paths["master"]
    slave_path = paths["slave"]

    # Extract label from identifier
    numbers = re.findall(r'\d+\.\d+|\d+', identifier)

    # Read the CSV files
    master_data = read_csv(master_path)
    slave_data = read_csv(slave_path)

    # Calculate delays
    delays_ms = calculate_delays(master_data, slave_data)

    # Filter outliers
    delays_ms = min_max_latencies(delays_ms)
    np.savez(directory + "Results/RESULT_VECTOR_" + identifier[:-4], delays = delays_ms)


def process_directory(directory):
    """Process all master-slave file pairs in a directory in parallel."""
    if not any(file.endswith(".npz") for file in os.listdir(directory + "Results/")):
        files = sorted(os.listdir(directory))
        pairs = {}
        for file in files:
            if "MASTER" in file or "SLAVE" in file:
                identifier = file.split("_MASTER_")[1] if "MASTER" in file else file.split("_SLAVE_")[1]
                if identifier not in pairs:
                    pairs[identifier] = {}
                if "MASTER" in file:
                    pairs[identifier]["master"] = os.path.join(directory, file)
                if "SLAVE" in file:
                    pairs[identifier]["slave"] = os.path.join(directory, file)

        markers = ["X", "v", "8", "D", "^", "*", "s", "<", "4", "H", "o", ">"]
        tasks = []
        with ProcessPoolExecutor() as executor:
            for counter, (identifier, paths) in enumerate(pairs.items()):
                if "master" in paths and "slave" in paths:
                    marker = markers[counter % len(markers)]
                    print(identifier)
                    tasks.append(executor.submit(process_pair, identifier, paths, marker, directory))

        for task in tasks:
            task.result()
        print("---------------------------------------------")

    process_npz_files(directory)


if __name__ == "__main__":
    # === Initialize plot ===
    plt.figure(figsize=(10, 6))

    # === Set experiment directory path ===
    directory = '../Exp5/'  # Adjust as needed

    # === Process and plot all results ===
    process_directory(directory)

    if LOG_SCALE:
        plt.yscale('log')
    plt.xlabel('Latency (ms)', fontsize=15)
    if PDF:
        plt.ylabel('PDF', fontsize=15)
    elif CCDF:
        if(LOG_SCALE):
            plt.ylabel('CCDF (log scale)', fontsize=15)
        else:
            plt.ylabel('CCDF', fontsize=15)
    else:
        if(LOG_SCALE):
            plt.ylabel('CDF (log scale)', fontsize=15)
        else:
            plt.ylabel('CDF', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend(loc='upper right', fontsize=15)
    plt.show()
