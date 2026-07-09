"""
Ross-OS Evidence Engine — Lorenz Benchmark Harness v2

Protocol: E-BMS-001-LZ-0001-P2
Purpose: Evaluate Geo-HEX v1.0 forecasting accuracy on Lorenz chaotic trajectories
Status: Active

This harness:
1. Generates deterministic Lorenz trajectories (seed=42)
2. Establishes baseline metrics
3. Integrates Geo-HEX v1.0 predictor (placeholder)
4. Captures horizon-specific RMSE, coverage, calibration
5. Exports protocol-versioned telemetry
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import uuid

import numpy as np
from scipy.integrate import solve_ivp


# ============================================================================
# LORENZ SYSTEM CONFIGURATION (E-BMS-001-LZ-0001)
# ============================================================================

LORENZ_CONFIG = {
    "sigma": 10.0,
    "rho": 28.0,
    "beta": 8.0 / 3.0,
    "dt": 0.01,
    "steps": 100_000,
    "seed": 42,
    "initial_state": [1.0, 1.0, 1.0],
}

# Forecast horizons (in steps)
HORIZONS = [1, 5, 10, 25, 50]

# Prediction intervals
PREDICTION_INTERVALS = [0.68, 0.95, 0.997]


# ============================================================================
# LORENZ ATTRACTOR
# ============================================================================

def lorenz_system(t, state, sigma, rho, beta):
    """Lorenz differential equations."""
    x, y, z = state
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]


def generate_trajectory(steps, dt, seed=42):
    """
    Generate deterministic Lorenz trajectory.
    
    Returns:
        trajectory: shape (steps, 3) — x, y, z coordinates
        metadata: dict with generation parameters
    """
    np.random.seed(seed)
    
    t_span = (0, steps * dt)
    t_eval = np.linspace(0, steps * dt, steps)
    
    sol = solve_ivp(
        lorenz_system,
        t_span,
        LORENZ_CONFIG["initial_state"],
        args=(LORENZ_CONFIG["sigma"], LORENZ_CONFIG["rho"], LORENZ_CONFIG["beta"]),
        t_eval=t_eval,
        method="RK45",
        dense_output=True,
    )
    
    trajectory = sol.y.T  # Shape: (steps, 3)
    
    metadata = {
        "generator": "scipy.integrate.solve_ivp",
        "method": "RK45",
        "steps": steps,
        "dt": dt,
        "sigma": LORENZ_CONFIG["sigma"],
        "rho": LORENZ_CONFIG["rho"],
        "beta": LORENZ_CONFIG["beta"],
        "seed": seed,
    }
    
    return trajectory, metadata


# ============================================================================
# BASELINE METRICS
# ============================================================================

def compute_rmse(y_true, y_pred):
    """Root mean squared error."""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def compute_lyapunov_max(trajectory, dt=0.01):
    """
    Estimate maximum Lyapunov exponent using small perturbations.
    For Lorenz (σ=10, ρ=28, β=8/3): expected ~0.90 ± 0.05
    """
    epsilon = 1e-8
    divergences = []
    
    for i in range(0, len(trajectory) - 100, 100):
        # Small perturbation
        perturbed_state = trajectory[i] + np.random.randn(3) * epsilon
        
        # Re-integrate from perturbed state
        t_span = (0, 10.0)
        t_eval = np.linspace(0, 10.0, 1000)
        
        sol = solve_ivp(
            lorenz_system,
            t_span,
            perturbed_state,
            args=(LORENZ_CONFIG["sigma"], LORENZ_CONFIG["rho"], LORENZ_CONFIG["beta"]),
            t_eval=t_eval,
            method="RK45",
        )
        
        perturbed_traj = sol.y.T
        original_segment = trajectory[i : i + len(perturbed_traj)]
        
        divergence = np.linalg.norm(perturbed_traj - original_segment, axis=1)
        divergences.extend(np.log(divergence / epsilon + 1e-10))
    
    if divergences:
        lyapunov = np.mean(divergences) / 10.0  # Normalize by integration time
        return max(0.0, lyapunov)
    return 0.0


def compute_trajectory_divergence(trajectory):
    """
    Max distance from any point on trajectory to attractor manifold.
    For Lorenz, attractor is roughly contained within [-20, 20]^3.
    """
    bounds = 20.0
    violations = np.sum(np.abs(trajectory) > bounds)
    max_distance = np.max(np.abs(trajectory)) - bounds if violations > 0 else 0.0
    return max_distance


# ============================================================================
# GEO-HEX PLACEHOLDER (INTEGRATION POINT)
# ============================================================================

def geo_hex_predict(trajectory, horizon, window_size=100):
    """
    Placeholder for Geo-HEX v1.0 predictor.
    
    In production, this integrates the real Geo-HEX model.
    For now, returns a simple autoregressive baseline.
    
    Args:
        trajectory: shape (n, 3) — full trajectory
        horizon: steps ahead to predict
        window_size: context window
    
    Returns:
        predictions: shape (n - window_size, 3) — point predictions
        intervals: dict of lower/upper bounds for each confidence level
    """
    n = len(trajectory)
    predictions = []
    
    # Simple autoregressive baseline: use last value with small noise
    for i in range(window_size, n - horizon):
        context = trajectory[i - window_size : i]
        last_state = context[-1]
        
        # Predict: last state + small drift
        pred = last_state + np.random.randn(3) * 0.01
        predictions.append(pred)
    
    predictions = np.array(predictions)
    
    # Placeholder intervals (will be replaced with real Geo-HEX intervals)
    intervals = {
        level: {
            "lower": predictions - 0.5,
            "upper": predictions + 0.5,
        }
        for level in PREDICTION_INTERVALS
    }
    
    return predictions, intervals


def compute_horizon_metrics(trajectory, horizons, window_size=100):
    """
    Compute RMSE and coverage for each forecast horizon.
    
    Returns:
        metrics_by_horizon: dict mapping horizon -> {rmse, coverage, ...}
    """
    metrics_by_horizon = {}
    
    for horizon in horizons:
        # Generate predictions
        predictions, intervals = geo_hex_predict(trajectory, horizon, window_size)
        
        # True values at horizon
        true_values = trajectory[
            window_size + horizon : window_size + horizon + len(predictions)
        ]
        
        if len(predictions) == 0 or len(true_values) == 0:
            continue
        
        # RMSE
        rmse = compute_rmse(true_values, predictions)
        
        # Coverage for each interval
        coverage = {}
        for level in PREDICTION_INTERVALS:
            lower = intervals[level]["lower"]
            upper = intervals[level]["upper"]
            
            # Check if true values fall within intervals
            in_interval = np.logical_and(true_values >= lower, true_values <= upper)
            cov = np.mean(in_interval)
            coverage[f"coverage_{int(level*100)}"] = float(cov)
        
        # Correlation
        flat_pred = predictions.flatten()
        flat_true = true_values.flatten()
        if len(flat_pred) > 1:
            correlation = np.corrcoef(flat_pred, flat_true)[0, 1]
        else:
            correlation = np.nan
        
        metrics_by_horizon[f"horizon_{horizon}"] = {
            "rmse": float(rmse),
            "correlation": float(correlation) if not np.isnan(correlation) else 0.0,
            **coverage,
        }
    
    return metrics_by_horizon


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute benchmark harness and generate telemetry."""
    
    print(f"[{datetime.now().isoformat()}] Initializing Evidence Engine — P2")
    print(f"Protocol: E-BMS-001-LZ-0001-P2")
    print(f"Harness: lorenz_benchmark_v2.py")
    
    # Generate trajectory
    print("\n[STEP 1] Generating deterministic Lorenz trajectory...")
    trajectory, gen_metadata = generate_trajectory(
        LORENZ_CONFIG["steps"],
        LORENZ_CONFIG["dt"],
        seed=LORENZ_CONFIG["seed"],
    )
    print(f"  Trajectory shape: {trajectory.shape}")
    print(f"  Bounds: x={trajectory[:, 0].min():.2f} to {trajectory[:, 0].max():.2f}")
    
    # Baseline metrics
    print("\n[STEP 2] Computing baseline metrics...")
    lyapunov = compute_lyapunov_max(trajectory)
    divergence = compute_trajectory_divergence(trajectory)
    print(f"  Lyapunov Max: {lyapunov:.4f} (expected: 0.90 ± 0.05)")
    print(f"  Trajectory Divergence: {divergence:.4f} (threshold: < 50)")
    
    # Horizon metrics
    print("\n[STEP 3] Computing horizon-specific metrics...")
    horizon_metrics = compute_horizon_metrics(trajectory, HORIZONS)
    for h, m in horizon_metrics.items():
        print(f"  {h}: RMSE={m['rmse']:.4f}, correlation={m['correlation']:.4f}")
    
    # Telemetry
    run_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    metrics = {
        "protocol": "E-BMS-001-LZ-0001-P2",
        "harness": "lorenz_benchmark_v2.py",
        "model": "geo_hex_v1.0",
        "run_id": run_id,
        "timestamp": timestamp,
        "seed": LORENZ_CONFIG["seed"],
        "metrics": {
            "lyapunov_max": float(lyapunov),
            "trajectory_divergence": float(divergence),
            **{k: v for h_metrics in horizon_metrics.values() for k, v in h_metrics.items()},
        },
        "audit_trail": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "numpy_version": np.__version__,
            "validation_status": "PASS" if lyapunov > 0.85 and divergence < 50 else "WARN",
        },
    }
    
    metadata = {
        "protocol": "E-BMS-001-LZ-0001-P2",
        "run_id": run_id,
        "timestamp": timestamp,
        "lorenz_config": LORENZ_CONFIG,
        "generation_metadata": gen_metadata,
        "horizons": HORIZONS,
        "prediction_intervals": PREDICTION_INTERVALS,
    }
    
    # Create results directory
    results_dir = (
        Path(__file__).parent.parent
        / "results"
        / "E-BMS-001-LZ-0001-P2"
        / run_id
    )
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Write telemetry
    print(f"\n[STEP 4] Writing telemetry to {results_dir}...")
    
    metrics_file = results_dir / "metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"  ✓ metrics.json written ({metrics_file.stat().st_size} bytes)")
    
    metadata_file = results_dir / "metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  ✓ metadata.json written ({metadata_file.stat().st_size} bytes)")
    
    # Store trajectory
    trajectory_file = results_dir / "trajectory.csv"
    np.savetxt(trajectory_file, trajectory, delimiter=",", header="x,y,z", comments="")
    print(f"  ✓ trajectory.csv written ({trajectory_file.stat().st_size} bytes)")
    
    print(f"\n[{datetime.now().isoformat()}] ✅ Benchmark complete")
    print(f"Run ID: {run_id}")
    print(f"Results: {results_dir}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
