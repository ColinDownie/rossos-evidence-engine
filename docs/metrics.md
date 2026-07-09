# Metrics

Formal definitions of all Evidence Engine metrics.

## Lorenz Baseline Metrics (E-BMS-001-LZ-0001-P1)

### RMSE (Root Mean Squared Error)
**Definition**: Root mean squared difference between computed trajectory and baseline reference.

$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - x_{ref,i})^2}$$

**Threshold**: < 0.001  
**Purpose**: Validates harness correctness and numerical stability.

### Lyapunov Maximum
**Definition**: Maximum Lyapunov exponent of the attractor.

For Lorenz (σ=10, ρ=28, β=8/3): Expected 0.90 ± 0.05

**Threshold**: 0.85 – 0.95  
**Purpose**: Confirms chaotic behavior within expected bounds.

### Trajectory Divergence
**Definition**: Maximum Euclidean distance from any point on trajectory to the Lorenz attractor manifold.

**Threshold**: < 50 units  
**Purpose**: Ensures trajectory remains on the attractor, no numerical blow-up.

### Step Duration
**Definition**: Wall-clock time per integration step (milliseconds).

**Threshold**: < 1.0 ms  
**Purpose**: Confirms computational efficiency and baseline reproducibility.

---

## Geo-HEX Forecasting Metrics (E-BMS-001-LZ-0001-P2)

### Horizon-Specific RMSE

**Horizon-1 RMSE**: 1-step ahead prediction error  
**Threshold**: < 0.05

**Horizon-5 RMSE**: 5-step ahead prediction error  
**Threshold**: < 0.20

**Horizon-10 RMSE**: 10-step ahead prediction error  
**Threshold**: < 0.50

**Horizon-25 RMSE**: 25-step ahead prediction error  
**Threshold**: < 2.0

**Horizon-50 RMSE**: 50-step ahead prediction error  
**Threshold**: < 5.0

**Formula**:
$$\text{RMSE}_h = \sqrt{\frac{1}{M} \sum_{j=1}^{M} (y_{t+h}^{pred} - y_{t+h}^{true})^2}$$

where $h$ is the forecast horizon and $M$ is the number of forecast points.

**Purpose**: Quantifies prediction accuracy at short, medium, and long ranges. Captures degradation of predictability with forecast lead time.

### Coverage (95% Prediction Interval)
**Definition**: Proportion of true values that fall within the 95% prediction interval.

$$\text{Coverage}_{95\%} = \frac{\text{# true values in interval}}{N} \times 100\%$$

**Threshold**: 90–95%  
**Purpose**: Validates whether prediction intervals are properly calibrated. Under-coverage (<90%) indicates overconfident predictions. Over-coverage (>95%) indicates overly conservative intervals.

### Correlation (Pearson r)
**Definition**: Pearson correlation coefficient between predicted and true trajectories.

$$r = \frac{\sum (y^{pred} - \bar{y}^{pred})(y^{true} - \bar{y}^{true})}{\sqrt{\sum (y^{pred} - \bar{y}^{pred})^2} \sqrt{\sum (y^{true} - \bar{y}^{true})^2}}$$

**Threshold**: > 0.80  
**Purpose**: Measures whether the predictor captures the true trajectory's dynamics and phase relationships, even if point-wise error is high.

### Calibration Error
**Definition**: Deviation of empirical coverage from nominal confidence level across all confidence levels.

$$\text{Calibration Error} = \max_{\alpha} |\text{Coverage}_{\alpha} - \alpha|$$

where α ∈ {0.68, 0.95, 0.997}

**Threshold**: < 0.05  
**Purpose**: Ensures prediction intervals are statistically honest across all confidence levels.

---

## Output Format

All metrics are stored in `metrics.json` with full metadata:

```json
{
  "protocol": "E-BMS-001-LZ-0001-P2",
  "harness": "lorenz_benchmark_v2.py",
  "model": "geo_hex_v1.0",
  "run_id": "<uuid>",
  "timestamp": "2026-07-09T10:00:00Z",
  "seed": 42,
  "metrics": {
    "horizon_1_rmse": 0.042,
    "horizon_5_rmse": 0.185,
    "horizon_10_rmse": 0.475,
    "horizon_25_rmse": 1.92,
    "horizon_50_rmse": 4.87,
    "coverage_95": 0.923,
    "correlation": 0.85,
    "calibration_error": 0.032
  },
  "audit_trail": {
    "environment": "Python 3.9.15, numpy 1.21.0, scipy 1.7.0",
    "duration_seconds": 847.3,
    "validation_status": "PASS"
  }
}
```

---

**This is your scientific measurement vocabulary.** Every metric is formally defined, thresholded, and auditable.
