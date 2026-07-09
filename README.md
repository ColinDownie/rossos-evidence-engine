# Ross‑OS Evidence Engine

A reproducible benchmark and telemetry system for validating Ross‑OS predictions against ground truth. This repository implements protocol‑versioned harnesses, Lorenz testbeds, baseline models, audit trails, and empirical metrics for scientific verification.

## Purpose

The Evidence Engine provides:
- **Protocol versioning** — Governs harness compatibility and metric definitions
- **Benchmark harnesses** — Executable reproducibility chains (Lorenz, future models)
- **Telemetry capture** — Structured metrics with complete audit trails
- **Results archive** — Versioned, reproducible runs stored with metadata
- **Geo‑HEX integration** — Horizon forecasting validation layer

## Core Sections

### [/protocols](./protocols) — Protocol Library
Versioned governance specifications:
- `E-BMS-001-LZ-0001-P1` — Lorenz baseline (Rössler stable)
- `E-BMS-001-LZ-0001-P2` — Lorenz with Geo‑HEX forecasting

Each protocol defines harness requirements, metric specifications, and reproducibility constraints.

### [/benchmarks](./benchmarks) — Harnesses
Executable benchmark implementations:
- `lorenz_benchmark_v2.py` — Primary Lorenz attractor validation
- Future: Rössler, Kuramoto, and stochastic models

### [/models](./models) — Predictor Integration
Geo‑HEX and baseline predictors:
- `geo_hex_v1/` — Horizon forecasting model
- Version management and compatibility tracking

### [/results](./results) — Telemetry Archive
Immutable run results organized by protocol:
```
results/
  E-BMS-001-LZ-0001-P2/
    <run_id>/
      metrics.json          # Protocol-defined metrics
      geo_hex_predictions.csv
      metadata.json         # Run environment, timestamps
```

### [/docs](./docs) — Scientific Documentation
- `metrics.md` — Formal metric definitions (RMSE, horizon distributions, etc.)
- `protocols.md` — Protocol change history and governance
- `reproducibility.md` — Environment setup and validation procedures

### [/notebooks](./notebooks) — Analysis Workspace
Jupyter notebooks for trajectory visualization, baseline comparison, and horizon distribution analysis.

### [/ci](./ci) — Continuous Evidence Pipeline
GitHub Actions workflows that:
- Install dependencies and environment
- Execute harnesses against protocol spec
- Capture and commit results
- Tag runs with protocol version

## Quick Start

1. **Read the protocol**: Check [/protocols](./protocols) for the harness specification.
2. **Run a benchmark**: See [/benchmarks](./benchmarks) for execution instructions.
3. **Review results**: Check [/results](./results) for previous runs.
4. **Understand metrics**: See [/docs/metrics.md](./docs/metrics.md) for formal definitions.

## Reproducibility Guarantees

All results include:
- Protocol version (governs harness behavior)
- Environment snapshot (Python, dependencies, seed state)
- Complete audit trail (timestamps, parameters, outputs)
- Metadata registry (run_id, executor, validation status)

See [/docs/reproducibility.md](./docs/reproducibility.md) for full reproducibility procedures.

## Versioning

- **Protocols** follow `E-BMS-001-<model>-<version>-P<protocol_revision>`
- **Harnesses** track implementation revisions
- **Results** are immutable, versioned by run_id and protocol

See [CHANGELOG.md](./CHANGELOG.md) for complete version history.

---

**This is a scientific instrument.** All changes are auditable, all results are reproducible, all metrics are formally defined.
