# Experiment 2: Delay Analysis Based on Offset between Transmission Windows of MS and SL Switches

<img width="1260" height="563" alt="image" src="https://github.com/user-attachments/assets/af627882-69f1-4a6c-b55f-2ba37d14ab4d" />

We analyze the effect on the empirical delay of the DC traffic of different temporal shifts between network cycles at MS and SL. TAS is similarly configured at both switches, with fixed transmission window of 46.5 μs and network cycle of 30 ms. We sweep offset between 5 ms, 10 ms, 15 ms, 20 ms, 25 ms, and 30 ms.

A critical finding is that the time offset, which is the delay between the start of transmission windows in consecutive switches, must be calculated based on high-order percentiles of the measured 5G delay (e.g., 99.9th percentile). On the one hand, if the offset is underestimated, packets frequently miss their window, causing Inter-Cycle Interference (ICI) and massive jitter. On the other hand, if the oggset is overestimated with a larger value, it provides a safety buffer against 5G jitter, but introduces unnecessary constant delay to the end-to-end communication, which may exceed the requirements of ultra-low-latency industrial applications.
