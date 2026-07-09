# E-BMS-001-LZ-0001-P2 — Lorenz with Geo-HEX Forecasting

**Status**: Active  
**Version**: 1.0  
**Created**: 2026-07-09  
**Harness**: `lorenz_benchmark_v2.py`  
**Predictor**: Geo-HEX v1.0

## Purpose

Validate Geo-HEX v1.0 forecasting accuracy against Lorenz chaotic trajectories. Measures prediction quality at multiple horizons, alignment with true dynamics, and forecast interval coverage.

## Harness Configuration

### Lorenz Parameters
- **sigma** (Prandtl): 10.0
- **rho** (Rayleigh): 28.0
- **beta**: 8.0 / 3.0
- **dt** (timestep): 0.01
- **steps**: 100,000
- **seed**: 42 (reproducible)

### Geo-HEX Configuration
- **Model**: Geo-HEX v1.0
- **Input Window**: 100 steps (1.0 time unit)
- **Forecast Horizons**: 1, 5, 10, 25, 50 steps ahead
- **Prediction Intervals**: 68%, 95%, 99.7%

## Metrics

| Metric | Definition | Threshold |
|--------|-----------|-----------|
| Horizon-1 RMSE | 1-step ahead prediction error | < 0.05 |
| Horizon-5 RMSE | 5-step ahead prediction error | < 0.20 |
| Horizon-10 RMSE | 10-step ahead prediction error | < 0.50 |
| Horizon-25 RMSE | 25-step ahead prediction error | < 2.0 |
| Horizon-50 RMSE | 50-step ahead prediction error | < 5.0 |
| Coverage 95% | % of true values in 95% prediction interval | 90-95% |
| Correlation | Pearson r between predicted and true trajectories | > 0.80 |
| Calibration | Prediction interval calibration error | < 0.05 |

## Expected Output

Results stored in: `results/E-BMS-001-LZ-0001-P2/<run_id>/`

```
metrics.json               # Protocol-defined metrics (all horizons)
geo_hex_predictions.csv    # Full prediction trace with intervals
trajectory.csv             # True Lorenz trajectory
metadata.json              # Environment, timestamps, seed state, model version
```

## Reproducibility Checklist

- [ ] Python 3.9+
- [ ] numpy >= 1.21
- [ ] scipy >= 1.7
- [ ] Geo-HEX v1.0 (exact version tagged)
- [ ] Seed fixed to 42
- [ ] dt = 0.01, steps = 100,000
- [ ] All parameters match tables above
- [ ] Input window = 100 steps
- [ ] Forecast horizons: 1, 5, 10, 25, 50

See [../../docs/reproducibility.md](../../docs/reproducibility.md) for full audit procedures.

---

**This is your validation protocol.** Geo-HEX sits on top of the Lorenz baseline and must prove its forecasting accuracy across multiple horizons. Every run is versioned against this exact specification.
