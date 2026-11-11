import json
from pathlib import Path

def test_control_packet_schema():
    packet_path = Path("common-schemas/control_packet.json")
    assert packet_path.exists()
    data = json.loads(packet_path.read_text())
    assert data["event"] == "update_params"
    payload = data["payload"]
    assert "baud_tx" in payload
    assert "baud_rx" in payload
    assert payload["baud_tx"] > 0
    assert payload["v_high"] > payload["v_low"]

def test_waveform_packet_schema():
    packet_path = Path("common-schemas/waveform_packet.json")
    assert packet_path.exists()
    data = json.loads(packet_path.read_text())
    assert data["event"] == "stream_frame"
    payload = data["payload"]
    assert "batch_id" in payload
    assert "time_delta_ms" in payload
    assert len(payload["raw_analog"]) == len(payload["filtered_binary"])
    assert len(payload["filtered_binary"]) == len(payload["strobe_ticks"])
    assert all(val in (0, 1) for val in payload["filtered_binary"])

def test_docs_integrity():
    arch_doc = Path("docs/SYSTEM_ARCHITECTURE.md")
    assert arch_doc.exists()
    content = arch_doc.read_text()
    assert len(content) > 100
