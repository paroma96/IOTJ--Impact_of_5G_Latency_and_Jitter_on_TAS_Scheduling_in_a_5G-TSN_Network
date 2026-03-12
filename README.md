# Impact of 5G Latency and Jitter on TAS Scheduling in a 5G-TSN Network: An Empirical Study

As Industry 4.0 moves towards flexible workflows and the use of 
Autonomous Mobile Robots (AMRs), integrating 5G with 
Time-Sensitive Networking (TSN) has become the next big frontier. 
However, the stochastic nature of 5G latency often clashes with 
the strict microsecond-level precision required by the industrial 
applications relying on IEEE 802.1Qbv Time-Aware Shaper (TAS), 
posing a significant challenge for end-to-end determinism.

In this study [1], we present an empirical evaluation using a 
real-world testbed with commercial 5G and TSN switches. The full 
TSN network is synchronized through TSN translators, i.e., NW-TT 
and DS-TT, located on both sides of the 5G system, resembling a 
real industrial 5G-TSN network. We analyzed how 5G downlink jitter 
impacts TAS scheduling and provided key insights on how to tune 
transmission window offsets to maintain bounded latency. Our 
findings offer a practical perspective for those designing hybrid 
architectures that aim to replace cables with 5G without losing TSN 
guarantees.

Post-print Available: https://arxiv.org/abs/2603.07309

IEEE Xplore: Not Available

[1] P. Rodriguez-Martin, O. Adamuz-Hinojosa, P. Muñoz, J. Caleya-Sanchez, 
and P. Ameigeiras, “Impact of 5G Latency and Jitter on TAS Scheduling in 
a 5G-TSN Network: An Empirical Study,” _IEEE Internet of Things Journal_, 
Mar. 2026, doi: 10.1109/JIOT.2026.3673410.

**If you use data/code from this repository, please cite our paper. Thanks!**

# Testbed description
<img width="1265" height="252" alt="image" src="https://github.com/user-attachments/assets/f2b0d4ab-8de8-48ba-b140-148ecf3f534d" />

To carry out our empirical analysis, we implemented the testbed 
depicted in figure above. Its components are described below.

**5G System**. The 5G network comprises a single gNB
and a 5G core, both implemented on a PC with a 50 MHz
PCIe Amarisoft Software Defined Radio (SDR) cards and
an AMARI NW 600 license. The gNB operates in the n78
band with 30 kHz subcarrier spacing and a bandwidth of
50 MHz. Data transmission uses a Time Division Duplex
(TDD) scheme with a pattern of four consecutive downlink
slots, four uplink slots, and two flexible slots. Although our
analysis focuses solely on downlink traffic, this configuration
reserves resources for uplink, enabling a realistic testbed
environment. Two UEs are deployed, each consisting of a
Quectel RM500Q-GL modem connected via USB to an Intel
NUC 10 (i7-10710U, 16 GB RAM, 512 GB SSD) running
Ubuntu 22.04. Experiments are conducted using one LABIFIX
Faraday cage, with gNB antennas connected to the SDR via
SMA connectors. Finally, although it is common to assign one
DS-TT per UE, this proof of concept simplifies the setup
by using a single DS-TT for both UEs. Similarly, we use a
single NW-TT for simplicity’s sake.

**TSN Network**. The TSN network is built using Safran’s
WR-Z16 switches. One switch operates as the MS, another as
the SL, and two additional switches act as TSN translators, i.e.,
NW-TT and DS-TT. The MS is directly connected to a Safran
SecureSync 2400 server, which provides the GM clock to the
SL for time synchronization. Since the 5G system operates
in PTP TC mode (implemented in TSN translators), an
auxiliary WR-Z16 switch, also synchronized via a second
SecureSync 2400, is used to distribute the 5G GM clock
between the TSN translators. Each WR-Z16 switch is based
on a Xilinx Zynq-7000 FPGA and a 1 GHz dual-core ARM
Cortex-A9, enabling high switching rates and low processing
delays under a Linux-based OS. The switches support IEEE
802.1Qbv TAS and VLANs, and include sixteen 1 GbE Small
Form-factor Pluggable (SFP) timing ports configurable as PTP
MS or SL. Each egress port provides four priority hardware
queues to separate the different traffic flows, with a maximum
buffer size of 6.6 kB per queue. This limits the number of
PCPs from 0 to 3, and also imposes a constraint on sustained
throughput, as exceeding the draining capacity leads to packet
drops. Additionally, timestamping probes on each port enables
high-precision latency measurements between the output ports
of the TSN nodes.

**Testbed Clock Synchronization**. Time synchronization be-
tween the TSN GM clock server and the MS is established via
coaxial cables carrying two signals: a Pulse Per Second (PPS)
pulse for absolute phase alignment and a 10 MHz reference
for frequency synchronization through oscillator disciplining.
Similarly, the auxiliary WR-Z16 switch is synchronized with
the 5G GM clock server using the same coaxial interface,
enabling accurate time distribution between the NW-TT and
DS-TT to enable the TC mode. In the testbed, the MS and SL
communicate PTP packets over IPv4 using unicast
User Datagram Protocol (UDP) and the E2E delay measure-
ment mechanism. The PTP transmission rate is configured to
1 packet per second.

**End Devices and Testbed Connections**. Two Ubuntu 22.04
LTS servers operate as packet generator with packETH tool
and sink, respectively. All components in the testbed are
interconnected using 1 Gbps optical fiber links, except for
the connections between the NW-TT-gNB, and DS-TT-UEs,
which use 1 Gbps RJ-45 Ethernet cables.

**Network Traffic**. At the 5G core network, two distinct
Data Network Names (DNNs) are configured to create separate
network slices for industrial traffic management. One carries
both PTP and DC flows, while the other handles BE flow,
enabling differentiated routing and resource allocation. The
5G network employs IP transport because the considered UE
operates without Ethernet-based sessions. To support Layer 2
industrial automation traffic over IP, a Virtual Extensible LAN
(VxLAN)-based tunneling mechanism is implemented,
with two VxLANs configured accordingly: one transporting
DC and PTP flows, and the other BE flow. Packets are tagged
with PCP values reflecting the relative priority among the
flows: PCP 3 for packets of the PTP flow, PCP 2 for DC flow
packets, and PCP 0 for BE flow packets. Additionally, within
the 5G network, 5QI values are assigned per flow’s packets,
with 80 for PTP and DC traffic, and 9 for BE traffic.

# Experimental Setup
We evaluate the packet transmission delay for the DC flow
across five experimental scenarios. Each scenario
analyzes a specific TAS configuration parameter to evaluate
its effect on the TSN system’s ability to tolerate 5G-induced
delay.

**Experiment 1:** _Delay Analysis of 5G Network_. We analyze
the effect of varying the traffic generation rate for delay-critical
traffic (DC) on the delay and jitter of the 5G network to determine 
the empirical delay for the DC packets and, with it, the uncertainty 
interval. For that, we sweep the packet generation rate for the
DC packets in 300 kbps increments from 350 kbps to 1.55 Mbps. 
For each rate, the transmission window is calculated based
on the lower bound defined by the number of packets times the 
individual transmission delay, ensuring compliance
with the WR-Z16’s buffer size limitation. This results in
transmission windows at MS ranging from 10.5 μs to 46.5 μs.
TAS is enabled at the MS, while at SL the output queue gate
remains open 100% of the time. This is done this way to
estimate the Zero-Wait-at-SL (ZWSL) empirical delay. The network 
cycle is fixed at 30 ms.

**Experiment 2:** _Delay Analysis based on Offset between
transmission windows of MS and SL Switches_. We analyze the
effect on the empirical delay of the DC traffic of different 
temporal shifts between network cycles at MS and SL. TAS is 
similarly configured at both switches, with fixed transmission 
window of 46.5 μs and network cycle of 30 ms. We sweep offset
between 5ms , 10 ms, 15 ms, 20 ms, 25 ms, and 30 ms.

**Experiment 3:** _Delay Analysis Based on Network Cycle_.
We study the influence of the network cycle on the empirical delay
of DC packets with a constant δ to analyze the scenarios described
in the article. The network cycle is varied in the range of 6 ms, 8 ms, 
10 ms, 12.5 ms, 15 ms, 17.5 ms, 20 ms, and 22.5 ms. Transmission windows 
are set to 9 μs, 12 μs, 15 μs, 18 μs, 22.5 μs, 25.5 μs, 30 μs, and 33 μs,
respectively, to keep the injected data rate into the 5G-TSNnetwork 
constant at 1.55 Mbps.

**Experiment 4:** _Delay Analysis considering Multiple Traffic
flows with Same-Priority_. We evaluate the packet transmission
delay when multiple distinct flows share the same priority
output queue. Firstly, TAS is enabled exclusively at the
MS, while at the SL, the output queue gate remains open
100% of the time, as in Experiment 1 to obtain the ZWSL empirical delay
for DC packets. The network cycle is fixed at 30 ms and, to
accommodate all the flows, transmission windows are set to
0.25 ms, 0.5 ms, 0.75 ms, 1 ms, 1.25 ms, 1.5 ms, 1.75 ms, forwarding
from 1 to 7 aggregated DC flows at source each and analyzing
the delay distribution for one of them. Then, we also configure
TAS at SL so that is equal to TAS at MS to characterize the empirical 
delay. The offset δ is constant according to previous experiments.

**Experiment 5:** _Delay Analysis Based on BE Traffic Load_.
We sweep the best-effort (BE) packet generation rates of 600 Mbps, 
650 Mbps, 700 Mbps, 750 Mbps, 800 Mbps, 850 Mbps, 900 Mbps, 950 Mbps, 
and 980 Mbps to analyze how the BE load affects the DC traffic ZWSL
empirical delay distribution. The network cycle is fixed to  30 ms 
and the transmission window is set only at MS, of 46.5μs.

Note the network cycle values, unlike the Cyclic-Synchronous 
applications, have been adapted to the capabilities of our
5G-TSN experimental setup and, with it, the flow constraints
to potentially avoid Inter-Cycle Interference (IC) at first and 
thus allow observable delay variation across experiments. The 
purpose of this work is not to replicate an exact industrial 
configuration but to analyze the interaction between 5G delay 
and jitter and TAS under a synchronized 5G-TSN network.

# Measured data
Each run of the experiments has been executed for 33 minutes, 
discarding the samples captured during the first 3 minutes to 
ensure stable synchronization between TSN devices after clock 
locking. This time interval allows us to capture an average of 
340,000 valid samples for a single DC flow.

# Acknowledgement
This work has been financially supported by the Ministry for Digital
Transformation and the Civil Service of the Spanish Government through
TSI-063000-2021-28 (6G-CHRONOS) project, and by the European Union
through the Recovery, Transformation and Resilience Plan - NextGenerationEU.
Additionally, this publication is part of grant PID2022-137329OBC43
funded by MICIU/AEI/10.13039/501100011033 and ERDF/EU, and part
of FPU Grant 21/04225 funded by the Spanish Ministry of Universities.


