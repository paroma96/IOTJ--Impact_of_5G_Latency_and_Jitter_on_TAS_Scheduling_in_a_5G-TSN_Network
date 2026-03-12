# Experiment 5: Delay Analysis Based on BE Traffic Load

<img width="1252" height="792" alt="image" src="https://github.com/user-attachments/assets/a821196c-24cb-4170-8c17-ad81708d3f96" />

We sweep the best-effort (BE) packet generation rates of 600 Mbps, 650 Mbps, 700 Mbps, 750 Mbps, 800 Mbps, 850 Mbps, 900 Mbps, 950 Mbps, and 980 Mbps to analyze how the BE load affects the DC traffic ZWSL empirical delay distribution. The network cycle is fixed to 30 ms and the transmission window is set only at MS, of 46.5 μs.

These results highlight the limited isolation between DC and BE traffic in the 5G system. Although a guard band prevents collisions in the TAS domain, the 5G system only provides relative prioritization via the 5QI configuration. Consequently, resources are still shared, and under high BE load, DC packets may experience increased
queuing delays due to buffer contention. Hence, the latency and jitter of the DC flow are substantially increased by the BE load, and the offset must be reviewed again.
