# Expermient 4: Delay Analysis considering Multiple Traffic flows with Same-Priority (Part 2)

<img width="1253" height="698" alt="image" src="https://github.com/user-attachments/assets/68befb1a-05f4-4ab0-b10d-dc7a4dfc0e64" />

We evaluate the packet transmission delay when multiple distinct flows share the same priority output queue. Firstly, TAS is enabled exclusively at the MS, while at the SL, the output queue gate remains open 100% of the time, as in Experiment 1 to obtain the ZWSL empirical delay for DC packets. The network cycle is fixed at 30 ms and, to accommodate all the flows, transmission windows are set to 0.25 ms, 0.5 ms, 0.75 ms, 1 ms, 1.25 ms, 1.5 ms, 1.75 ms, forwarding from 1 to 7 aggregated DC flows at source each and analyzing the delay distribution for one of them. Then, we also configure TAS at SL so that is equal to TAS at MS to characterize the empirical delay. The offset δ is constant according to previous experiments.

The analysis shows that additional delay-critical traffic flows can degrade the performance of the deterministic flow if the 5G network does not implement strict traffic isolation. High-load scenarios increase the need for larger offsets to maintain deterministic transmissions across the 5G-TSN network.


