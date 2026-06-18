# SynthScope: System Architecture & Technical Deep-Dive

This document details the underlying engineering, physics modeling, and software architecture powering the SynthScope logic analyzer engine.

## 1. System Topology

SynthScope operates on a decoupled client-server architecture to ensure high-frequency UI rendering does not block heavy mathematical operations.

* **Client (Next.js / HTML5 Canvas):** Dedicated exclusively to rendering the incoming high-speed data stream at 60 FPS and capturing user control inputs.
* **Server (FastAPI / WebSockets):** Manages asynchronous client connections.
* **Logic Engine (Python / NumPy):** A standalone module ingested by the server that handles all signal generation, degradation modeling, and decoding.

## 2. Mathematical Modeling & Signal Processing

### A. Signal Synthesis
Digital signals are generated as mathematically ideal arrays. For a standard UART frame, the data byte is packed with framing bits:
* `[Start Bit (0)] + [Data Bits] + [Optional Parity] + [Stop Bit (1)]`
This bitstream is upsampled to represent a continuous physical line state over time.

### B. Physical Layer Degradation (Noise Injection)
Real-world jumper wires and breadboards introduce electromagnetic interference and impedance mismatches. We model this by treating the discrete binary states as an analog voltage level ($0V$ to $3.3V/5V$). 

Gaussian noise is injected continuously across the array:
`Y[n] = X[n] + N(μ, σ²)`
Where variance (`σ²`) is controllable in real-time via the frontend to simulate varying levels of environmental noise.

### C. Software Signal Conditioning
To accurately decode the analog waveform back into digital logic, SynthScope implements a software-based **Schmitt Trigger**. 
Unlike a simple threshold comparator, the Schmitt Trigger utilizes hysteresis to prevent "chattering" (rapid false transitions) caused by noise near the logic threshold. 
* State transitions to Logic High (`1`) only occur when voltage exceeds $V_{high}$.
* State transitions to Logic Low (`0`) only occur when voltage drops below $V_{low}$.

### D. Protocol Decoding State Machine
The conditioned, binary array is passed to a software edge-detector. Sampling occurs based on the user-defined receiver baud rate ($Baud_{rx}$). Desynchronization between $Baud_{tx}$ and $Baud_{rx}$ causes the state machine to sample at incorrect intervals, visually demonstrating framing errors and data corruption.

## 3. Data Flow & Contracts

Communication between the frontend and backend strictly adheres to predefined JSON schemas over WebSockets to minimize overhead. 

* **Control Payloads (Client -> Server):** Transmits parameter updates (Baud rates, noise variance, threshold voltages) triggered by UI sliders.
* **Telemetry Streams (Server -> Client):** Batched point arrays containing the Raw Analog, Filtered Binary, and Strobe Tick indices, ensuring the Canvas API can draw continuous waveforms without frame-dropping.

## 4. Professional Toolchain Integration
To ensure SynthScope is a valid engineering tool rather than a toy, all session data can be serialized into the **IEEE 1364 standard VCD (Value Change Dump)** format. This allows seamless integration with industry-standard analysis software like GTKWave.
