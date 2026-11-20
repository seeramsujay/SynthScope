# SynthScope: Architectural Review & Engineering Roadmap (future.md)

---

## 1. Architectural Code Review & Current State Analysis

SynthScope provides an accessible, browser-first digital logic analyzer and physical layer synthesis platform. It allows electrical and computer engineering students and firmware engineers to visualize signal degradation, tune hysteresis thresholds, and export standard IEEE 1364 Value Change Dump (VCD) waveforms without dedicated benchtop oscilloscopes.

### Key Architectural Strengths
- **Decoupled Architecture:** Clean separation of concerns between Next.js (App Router) for the presentation/canvas layer and FastAPI for computational signal synthesis.
- **Parametric Hysteresis Engine:** Explicit dual-threshold software Schmitt Trigger conditioning cleanly models analog-to-digital domain transitions with configurable upper ($V_{TH}$) and lower ($V_{TL}$) trip points.
- **IEEE 1364 Interoperability:** Generates native `.vcd` files compatible with industry standard tools (GTKWave, PulseView, ModelSim, and Sigrok).

### Technical Debt & Optimization Bottlenecks
1. **Python Math Engine Throughput:** The existing numpy/scipy continuous waveform synthesis path suffers from GIL contention and memory allocation overhead when scaling to $>10^6$ sample points or multi-channel captures ($>8$ channels).
2. **Canvas 2D Rendering Bounds:** The current HTML5 Canvas 2D rasterizer struggles with high-density zoom/pan interactions across millions of sample cycles.
3. **Single-Protocol Coupling:** Logic decoding is currently hardcoded for UART framing (8N1, variable baud), lacking a plugin-based protocol decoding pipeline.

---

## 2. Strategic Engineering Roadmap

```mermaid
flowchart TD
    subgraph Phase 1: High-Performance Engine
        P1A[WebAssembly Rust DSP Kernel] --> P1B[WebGL / WebGPU Waveform Renderer]
        P1B --> P1C[Zero-Copy SharedArrayBuffer Ingestion]
    end

    subgraph Phase 2: Multi-Protocol Decoder Suite
        P2A[Protocol Decoders: I2C / SPI / CAN / 1-Wire] --> P2B[Packet Level State Machine Disassembler]
        P2B --> P2C[Protocol Search & Bookmark Engine]
    end

    subgraph Phase 3: Hardware Ingestion & Physical Probes
        P3A[WebSerial / WebUSB Driver] --> P3B[RP2040 PIO Logic Probe Firmware]
        P3B --> P3C[RTL-SDR / HackRF USB RF Baseband Bridge]
    end

    subgraph Phase 4: Autonomous Telemetry & AI Inspection
        P4A[Automated Timing Violation Assertions] --> P4B[Jitter & Eye Diagram Analysis]
        P4B --> P4C[LLM Protocol Reverse-Engineering Assistant]
    end

    Phase 1 --> Phase 2
    Phase 2 --> Phase 3
    Phase 3 --> Phase 4
```

---

## 3. Detailed Milestone Execution Plan

### Milestone 1: High-Performance Wasm DSP Core & WebGPU Canvas
- [ ] **Wasm Signal Synthesizer (Rust):** Port the Gaussian noise injection, analog filtering, and Schmitt trigger hysteresis calculation into a compiled WebAssembly module (`synthscope-core-wasm`).
- [ ] **GPU Accelerated Rendering:** Implement a WebGPU-based signal timeline capable of rendering $10^7$ discrete logic transitions at locked 60 FPS with dynamic Level of Detail (LoD) downsampling.
- [ ] **Real-time Memory Ring Buffer:** Utilize `SharedArrayBuffer` with Web Workers for non-blocking telemetry streaming between the synthesis worker and UI.

### Milestone 2: Extensible Protocol Decoder Ecosystem
- [ ] **Standard Decoders:**
  - **I2C:** Address ACK/NACK detection, 7-bit/10-bit addressing, clock stretching monitor.
  - **SPI:** Modes 0-3 ($CPOL$, $CPHA$), multi-slave Select ($SS$) decoding.
  - **CAN 2.0B & CAN-FD:** Dominant/Recessive bit framing, CRC verification, payload extraction.
  - **1-Wire & Manchester:** Pulse-width modulated timing recovery.
- [ ] **Custom Decoder API:** Expose a declarative JSON / WebAssembly interface allowing users to define proprietary synchronous/asynchronous packet decoders.

### Milestone 3: Hardware Ingestion & Edge Probe Integration
- [ ] **RP2040 8-Channel PIO Probe:** Develop an open-source firmware for the Raspberry Pi Pico (RP2040) capturing 8 digital channels up to 100 MSa/s streamed directly into SynthScope via WebSerial.
- [ ] **WebUSB / Sigrok Bridge:** Integrate WebUSB support for Saleae Logic, FX2LP, and Sigrok-compatible hardware logic analyzers.
- [ ] **RTL-SDR RF Demodulation:** Ingest raw I/Q samples from software-defined radios and decode 433 MHz / 868 MHz ASK/FSK industrial sensor data directly into the logic timeline.

### Milestone 4: Diagnostic Intelligence & Autonomous Verification
- [ ] **Eye Diagrams & Jitter Analysis:** Calculate Time-Interval Error (TIE), cycle-to-cycle jitter, and construct real-time eye diagrams to evaluate physical bus health.
- [ ] **Formal Protocol Assertions:** Pre-configured rule sets to detect setup/hold time violations, invalid start/stop bits, glitch pulses shorter than clock thresholds, and bus contention.
- [ ] **AI-Assisted Trace Explainer:** Context-aware diagnostic assistant that highlights corrupted checksums or timing drift and suggests concrete electrical fixes (e.g., lower pull-up resistance, ground loop isolation).
