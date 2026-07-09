---
title: "Fix lyapunov estimator shape guard and improve error visibility"
labels:
  - patch
---

Fixes a shape-mismatch in the Lyapunov estimator that caused CI failures; adds solver success and shape checks, clamps divergences, and enables full traceback printing for debugging in CI.
