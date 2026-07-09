# E-BMS-001-LZ-0001-P1 — Lorenz Baseline (Rössler Stable)

**Status**: Stable baseline  
**Version**: 1.0  
**Created**: 2026-07-09  
**Harness**: `lorenz_benchmark_v2.py`

## Purpose

Establish reproducible baseline for Lorenz attractor chaotic trajectory generation. No forecasting layer. Validates harness correctness and environment stability.

## Harness Configuration

### Parameters
- **sigma** (Prandtl): 10.0
- **rho** (Rayleigh): 28.0
- **beta**: 8.0 / 3.0
- **dt** (timestep): 0.01
- **steps**: 100,000
- **seed**: 42 (reproducible)

### Initial Conditions
- **x0**: 1.0
- **y0**: 1.0
- **z0**: 1.0

## Metrics

| Metric | Definition | Threshold |
|--------|-----------|-----------|
| RMSE | Root mean squared error vs. baseline trajectory | < 0.001 |
| Lyapunov Max | Maximum Lyapunov exponent | 0.90 ± 0.05 |
| Trajectory Divergence | Max distance from expected attractor | < 50 |
| Step Duration | Time per iteration (ms) | < 1.0 |

## Expected Output

Results stored in: `results/E-BMS-001-LZ-0001-P1/<run_id>/`

```
metrics.json          # Protocol-defined metrics
trajectory.csv        # Full x,y,z trace
metadata.json         # Environment, timestamps, seed state
```

## Reproducibility Checklist

- [ ] Python 3.9+
- [ ] numpy >= 1.21
- [ ] scipy >= 1.7
- [ ] Seed fixed to 42
- [ ] dt = 0.01, steps = 100,000
- [ ] All parameters match table above

See [../../docs/reproducibility.md](../../docs/reproducibility.md) for full audit procedures.

---

**This is your control baseline.** It has no predictor, no integration layer, just pure deterministic Lorenz chaos. All other protocols build on top of this.
