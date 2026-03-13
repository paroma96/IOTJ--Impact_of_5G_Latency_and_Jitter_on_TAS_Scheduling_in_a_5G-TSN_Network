This directory contains the suite of Python scripts used to process, analyze, 
and visualize the data obtained from the 5G-TSN testbed. These tools are 
essential for replicating the results presented in the paper regarding the 
impact of 5G non-determinism on Time-Aware Shaper (TAS) scheduling.

1. _compute_latencies_multi_experiments.py_:
This script is an automated data processing pipeline designed to calculate
and visualize communication delays for the experiments presented in the paper.
It synchronizes MS and SL CSV files by matching unique packet sequence numbers,
calculating the point-to-point latency as $L = T_{slave} - T_{master}$ in
milliseconds. To handle large datasets efficiently, it employs parallel processing
via ProcessPoolExecutor and caches results in .npz format. Additionally, the script
features an intelligent labeling system that uses Regex to extract experimental
parameters (like window sizes $W$ or bitrates $R$) directly from filenames,
automatically generating publication-quality plots of CDF, CCDF, or PDF distributions
with adaptive logarithmic scaling and LaTeX-formatted legends.
   
2. _figure1_delay_analysis_of_5G_Network.py_:   
This script, specifically designed for Experiment 1 (Exp1), focuses on generating a
publication-quality Cumulative Distribution Function (CDF) plot for empirical packet
transmission delays. It loads pre-computed latency vectors from .npz files and uses
LaTeX integration to render precise mathematical labels for various window
configurations ($W_{\mathrm{MS,DC}}$). The script's standout feature is the inclusion
of a high-resolution zoom, which provides a detailed view of the distribution's tail
behavior (latencies between 13 and 17.5 ms). By utilizing distinct line styles and a
two-column legend, it ensures that the performance differences between sub-millisecond
configurations are visually clear and suitable for a scientific journal.

4. _figure2_delay_analysis_based_on_offset_MS-SL.py_:
This script, tailored for Experiment 2 (Exp2), analyzes how packets are distributed
across successive transmission windows (network cycles) based on the TAS offset ($\delta_{\text{DC}}$).
It categorizes empirical delays into discrete windows by calculating the index
$k = \lfloor (d - \text{offset}) / \delta_{DC} \rfloor + 1$. The script generates a
sophisticated overlaid bar chart where each bar represents a TAS configuration, and
color-coded segments indicate the delay boundaries for the first, second, and third
transmission windows. Crucially, it calculates and annotates the exact probability of
a packet falling into each network cycle, providing a clear visual representation of
network reliability and the likelihood of packets being deferred to subsequent network
cycles as the offset varies.

6. _figure3_delay_analysis_based_on_network_cycle.py_:
This script, designed for Experiment 3 (Exp3), analyzes the impact of varying both the
network cycle time ($T_i^{\text{nc}}$) and the TAS window size ($W_{i,\text{DC}}$) on
packet transmission delays. It functions by grouping empirical delay data into
histograms to identify peaks representing discrete transmission windows. The code
employs a robust regex parser to extract these physical parameters from LaTeX-formatted
labels and sorts the results to demonstrate how increasing network cycle times linearly
extend the potential delay. The resulting visualization is a multi-parameter bar chart
where each configuration displays overlaid color-coded bars for successive network cycles,
topped with floating text annotations that specify the exact probability (Prob.) of a
packet being transmitted within that specific window.

8. _figure4_1_delay_analysis_multiple_same-priority_flows.py_:  
This script, tailored for Experiment 4 part 1 (Exp4_1), generates a high-precision Cumulative
Distribution Function (CDF) plot to analyze the impact of significantly larger TAS window
sizes ($W_{\mathrm{MS,DC}}$ ranging from 0.25 to 1.75 ms) on packet transmission delays.
It utilizes a wide array of distinct line styles and a specific dashed pattern for the
final dataset to ensure visual clarity across multiple curves. Similar to the $Exp1$ script,
it incorporates a sophisticated zoom inset positioned in the upper-left corner, but with
specialized formatting: the inset Y-axis is shifted to the right and uses a formatter
to display four decimal places, allowing for an extremely granular inspection of the
distribution's tail (latencies between 16 and 23 ms). This visualization highlights how
larger window configurations affect the deterministic bounds of the system.

9. _figure4_2_delay_analysis_multiple_same-priority_flows.py_: 
This script, designed for Experiment 4 part 2 (Exp4_2), focuses on analyzing the drawn tails
behavior of latencies by plotting the Complementary Cumulative Distribution Function (CCDF) on
a logarithmic scale. To handle the large gap between typical packet delays and extreme outliers,
it implements a broken-axis visualization, splitting the x-axis into two segments: one for the
primary delay region (18–21.6 ms) and another for the distant tail (48–51 ms). It also
features a logarithmic zoom inset that specifically targets the 20 ms transition threshold. By
hiding internal spines and adding diagonal markers, the script provides a publication-ready view
of how different window sizes ($W_{i,DC}$) impact the probability of rare, high-latency events
across discontinuous time intervals.

10. _figure5_delay_analysis_based_on_BE_traffic_load.py_:
This script, tailored for Experiment 5 (Exp5), investigates the impact of background traffic
congestion on latency by analyzing the Complementary Cumulative Distribution Function (CCDF) on a
logarithmic scale. It evaluates various injection rates of Best Effort traffic ($R_{BE}^{gen}$),
ranging from 600 to 980 Mbps. To effectively visualize both the deterministic performance and
the extreme jitter caused by high network load, the script utilizes a broken-axis layout
(3:1 ratio) that skips the inactive interval between 21 ms and 45 ms. This allows for a clear
comparison of the tails in the distribution, showing how increasing background traffic
elevates the probability of packets experiencing delays in much later network cycles, all
while maintaining LaTeX-quality formatting and distinct line styles for each traffic profile.
