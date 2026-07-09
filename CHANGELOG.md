# Changelog

All notable changes to the Evidence Engine are documented here.

## [Unreleased]

### Added
- Initial Evidence Engine architecture
- Protocol versioning framework (E-BMS-001 series)
- Lorenz benchmark harness (v2)
- Geo-HEX v1.0 predictor integration layer
- Results telemetry archive structure
- GitHub Actions continuous evidence pipeline

### Protocol Versions
- `E-BMS-001-LZ-0001-P1` — Lorenz baseline (Rössler stable attractor)
- `E-BMS-001-LZ-0001-P2` — Lorenz with Geo-HEX forecasting layer

### Harness Versions
- `lorenz_benchmark_v2.py` — Primary implementation, reproducible trajectory generation

---

## [Version 1.0.0] — 2026-07-09

### Initial Release
- Core Evidence Engine framework
- Protocol governance structure
- Benchmark harness architecture
- Telemetry capture and archival
- Reproducibility guarantees and audit trails

---

**Format**: This changelog follows [Keep a Changelog](https://keepachangelog.com/).  
**Versioning**: Protocols follow semantic versioning. Harnesses track implementation revisions independently.
