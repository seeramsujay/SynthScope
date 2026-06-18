### Step 1: The WebSocket Merge
- [ ] Kill the frontend mock service (Track 1.1) and the backend dummy generator (Track 2.2).
- [ ] Route Track 3's mathematical NumPy engine outputs directly into Track 2's WebSocket broadcast manager.
- [ ] Point Track 1's frontend Canvas directly to the localhost WebSocket port. 
- [ ] **Verification:** Validate that adjusting the frontend UI sliders successfully alters the analog noise floor on the Canvas in real-time.

### Step 2: Telemetry Validation
- [ ] Navigate the local application extensively.
- [ ] Access the telemetry dashboard and verify the context graph successfully maps DOM event candidates (slider drags, VCD export clicks) without breaking the Canvas rendering loop.

### Step 3: IDE Orchestration
- [ ] Activate backend debugging plugins. 
- [ ] Verify developers can query real-time session logs to instantly debug protocol misalignments (e.g., frontend requests a baud rate the backend logic engine rejects).
