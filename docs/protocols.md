# Protocols

Ross-OS Evidence Engine — Protocol Index

A complete index of all benchmark protocols maintained within the Evidence Engine. Each protocol is versioned, reproducible, and bound by the Ross-OS governance invariant: *Experiment → Measurement → Observation → Interpretation*.

## Active Protocols

### E-BMS-001-LZ-0001-P1
**Domain**: Lorenz System  
**Purpose**: Establish baseline harness behaviour and validate deterministic trajectory generation.  
**Status**: Archived (Superseded by P2)  
**Artifacts**:
- `lorenz_benchmark_v1.py`
- `metrics.json`
- `metadata.json`

See [../protocols/E-BMS-001-LZ-0001-P1/README.md](../protocols/E-BMS-001-LZ-0001-P1/README.md)

---

### E-BMS-001-LZ-0001-P2
**Domain**: Lorenz System + Geo-HEX v1.0  
**Purpose**: Evaluate Geo-HEX forecasting accuracy across multiple horizons and prediction intervals.  
**Status**: Active  
**Artifacts**:
- `lorenz_benchmark_v2.py`
- `metrics.json`
- `geo_hex_predictions.csv`
- `metadata.json`

See [../protocols/E-BMS-001-LZ-0001-P2/README.md](../protocols/E-BMS-001-LZ-0001-P2/README.md)

---

## Protocol Structure

Each protocol follows the same structural template:

1. **Header**
   - Protocol ID
   - Version
   - Status
   - Created date
   - Harness
   - Predictor (if applicable)

2. **Purpose**
   Defines the scientific intent and evaluation scope.

3. **Configuration**
   - System parameters
   - Model parameters
   - Input windows
   - Forecast horizons
   - Seeds
   - Thresholds

4. **Metrics**
   - RMSE
   - Horizon breach
   - Coverage
   - Calibration
   - Correlation

5. **Expected Outputs**
   Versioned telemetry stored under:
   ```
   results/<protocol>/<run_id>/
   ```

6. **Governance Notes**
   - No custom metrics unless mathematically validated
   - No symbolic interpretation in measurement blocks
   - Strict reproducibility requirements

---

## Versioning Rules

- **P1 → P2 transitions** occur only when harness logic, metric definitions, or model integration changes.
- Each protocol version is immutable once published.
- All telemetry must reference the exact protocol version used.

---

**This is your governance spine.** Every protocol is versioned, frozen, and auditable.
