#ASYNC TASK ROADMAP (GRANULAR & ISOLATED)

### Track 1: UI/UX & Frontend Integration Lead
- [ ] **Task 1.1:** Scaffold Next.js application. Set `export const runtime = 'edge'` in `layout.tsx`. Implement a mock WebSocket service emitting hardcoded `stream_frame` JSON payloads at 60Hz.
- [ ] **Task 1.2:** Build the `WaveformCanvas.tsx` component. Use native HTML5 Canvas API (via React `useRef`) to draw three vertically stacked timelines: Raw Analog, Filtered Binary, and Strobe Ticks. Connect to the mock WS stream.
- [ ] **Task 1.3:** Build the Control Panel component using Shadcn UI sliders for Baud Rate, Noise Variance, DC Offset, V_high, and V_low. Tie inputs to emit the `update_params` JSON schema.
- [ ] **Task 1.4:** Inject telemetry tracking scripts into the root layout `<body>` tag to index user interactions.

### Track 2: Backend & Routing Architect
- [ ] **Task 2.1:** Scaffold FastAPI application. Implement `ConnectionManager` class to handle WebSocket connect, disconnect, and broadcast methods.
- [ ] **Task 2.2:** Build a dummy generator loop using `asyncio.sleep(0.016)` (~60fps) that yields random float arrays matching the Outgoing Waveform schema and broadcasts them.
- [ ] **Task 2.3:** Implement the `/openapi.json` route to generate openapi-fetch TypeScript bindings for the frontend.
- [ ] **Task 2.4:** Configure strict CORS middleware in FastAPI to allow WebSocket upgrades/REST calls from localhost and the production domain.

### Track 3: Data Engineering & ECE Logic Lead
- [ ] **Task 3.1:** Write the `SignalGenerator` class in Python. Accept a binary payload and synthesize a square wave NumPy array enforcing UART protocols (Start bit 0, 8 data bits LSB first, Stop bit 1).
- [ ] **Task 3.2:** Implement continuous analog upsampler (16x default) and write the Gaussian noise injection function.
- [ ] **Task 3.3:** Implement Software Schmitt Trigger logic using a dual-threshold state machine over the NumPy array (transition high at 2.0V, transition low at 0.8V).
- [ ] **Task 3.4:** Write the Edge-Detection Protocol Decoder that samples the binary array at RX Baud, rebuilds the ASCII string, and logs framing errors.
- [ ] **Task 3.5:** Write the IEEE 1364 VCD export script. Format timestamps and state changes into valid `.vcd` strings and expose as a file download.

### Track 4: Cloud Ops & Systems IT Lead
- [ ] **Task 4.1:** Write a highly optimized, multi-stage Dockerfile for the FastAPI backend (slim python base, NumPy prerequisites, CMD to Uvicorn).
- [ ] **Task 4.2:** Provision cloud hosting configuration (e.g., Fly.toml) targeting the optimal region. Configure internal ports and health checks.
- [ ] **Task 4.3:** Setup the serverless Postgres database over a secure mesh network for storing exported waveforms/session data.
- [ ] **Task 4.4:** Initialize IDE server plugins (e.g., MCP) to connect real-time local development tools.
