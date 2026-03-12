# Experiment 3: Delay Analysis Based on Network Cycle

<img width="1261" height="547" alt="image" src="https://github.com/user-attachments/assets/8d9aee70-7f2a-4236-9c1b-9887ec6c6745" />

We study the influence of the network cycle on the empirical delay of DC packets with a constant δ to analyze the scenarios described in the article. The network cycle is varied in the range of 6 ms, 8 ms, 10 ms, 12.5 ms, 15 ms, 17.5 ms, 20 ms, and 22.5 ms. Transmission windows are set to 9 μs, 12 μs, 15 μs, 18 μs, 22.5 μs, 25.5 μs, 30 μs, and 33 μs, respectively, to keep the injected data rate into the 5G-TSNnetwork constant at 1.55 Mbps.

The results indicate that the TAS-configured network cycle must be strictly greater than the sum of the peak-to-peak jitter introduced by the 5G network plus the duration of the transmission window itself. If the 5G jitter exceeds this threshold, packets from one cycle can "overlap" with the next, causing Inter-Cycle Interference (ICI) and making it impossible to guarantee isolated and deterministic delivery.
