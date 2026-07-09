# Protocol Library

Versioned governance specifications for Evidence Engine harnesses and metrics.

## Active Protocols

### E-BMS-001-LZ-0001-P1
**Lorenz Baseline — Rössler Stable**

- **Status**: Stable
- **Created**: 2026-07-09
- **Harness**: `lorenz_benchmark_v2.py`
- **Model**: Lorenz attractor, chaotic regime
- **Forecast Integration**: None (baseline only)
- **Metric Set**: RMSE, trajectory divergence, Lyapunov exponents

See [./E-BMS-001-LZ-0001-P1/README.md](./E-BMS-001-LZ-0001-P1/README.md) for full specification.

---

### E-BMS-001-LZ-0001-P2
**Lorenz with Geo-HEX Forecasting**

- **Status**: Active
- **Created**: 2026-07-09
- **Harness**: `lorenz_benchmark_v2.py`
- **Model**: Lorenz attractor + Geo-HEX v1.0 predictor
- **Forecast Integration**: Horizon-based prediction validation
- **Metric Set**: RMSE, horizon accuracy, prediction intervals, geo-hex alignment

See [./E-BMS-001-LZ-0001-P2/README.md](./E-BMS-001-LZ-0001-P2/README.md) for full specification.

---

## Governance

All protocol changes trigger:
1. Harness update review
2. Metric definition audit
3. Reproducibility revalidation
4. Results re-archival with new protocol tag

See [../docs/protocols.md](../docs/protocols.md) for governance procedures.

---

**This is your benchmark governance spine.** Each protocol defines what the harness will measure, how it will measure it, and how results will be archived.
