# Reproducibility

Ross-OS Evidence Engine — Reproducibility Standard

The Ross-OS Evidence Engine enforces strict reproducibility guarantees for all benchmark runs. Every experiment must be fully reconstructible from code, configuration, and metadata alone. No telemetry is valid unless it can be regenerated under identical conditions.

## 1. Deterministic Execution

All benchmarks must specify:

- **Random seed**
- **Integration method**
- **Timestep (dt)**
- **Initial state generation method**
- **Model version**
- **Protocol version**

These values must appear in `metadata.json`.

---

## 2. Environment Capture

Each run must record:

- Python version
- NumPy version
- SciPy version
- Operating system
- Processor
- Timestamp
- Run ID

This ensures cross-machine reproducibility.

---

## 3. Harness Integrity

Benchmark harnesses must:

- Use fixed Lorenz parameters
- Use identical train/test splits
- Use isolated inference timing
- Export all predictions
- Export all metrics
- Export full metadata

Harnesses are versioned and stored under:

```
benchmarks/
```

---

## 4. Telemetry Requirements

Every run must produce:

- `metrics.json`
- `geo_hex_predictions.csv` (if applicable)
- `metadata.json`

Telemetry must be stored under:

```
results/<protocol>/<run_id>/
```

Each run is immutable.  
No telemetry may be overwritten.

---

## 5. Scientific Discipline

The Evidence Engine enforces:

- No fabrication
- No symbolic interpretation in measurement blocks
- No custom metrics without mathematical validation
- Strict separation of observation and interpretation

This ensures the scientific envelope remains intact.

---

## 6. Reproduction Procedure

To reproduce any run:

1. Clone the repository
2. Open the protocol sheet
3. Execute the associated harness
4. Verify environment metadata
5. Compare outputs with stored telemetry

If all values match within numerical tolerance, the run is reproducible.

---

## 7. CI Reproducibility

GitHub Actions may be used to:

- Re-run benchmarks
- Validate telemetry
- Confirm environment consistency
- Publish new protocol versions

CI runs must reference the exact protocol version.

---

**This is your reproducibility guarantee.** Every run is auditable, every metric is verifiable, every protocol is frozen.
