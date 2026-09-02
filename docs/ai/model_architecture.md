# THGNN Model Architecture

## Overview

The Temporal Heterogeneous Graph Neural Network (THGNN) combines:
1. **Heterogeneous Graph Attention** for multi-type node/edge reasoning
2. **Temporal Encoding** for time-aware pattern detection
3. **Explainability** for interpretable threat explanations

## Architecture

```
Input: Temporal Heterogeneous Graph (PyG HeteroData)
    ↓
Node Encoder (type-specific linear projections)
    ↓
Temporal Encoder (Time2Vec / sinusoidal positional)
    ↓
HGAT Layer 1 (heterogeneous graph attention)
    ↓
HGAT Layer 2 (with residual connections)
    ↓
HGAT Layer 3 (with residual connections)
    ↓
Readout (user-level aggregation)
    ↓
MLP Classifier → Threat Score [0, 1]
```

## Hyperparameters

See `configs/model.yaml` for full configuration.

TODO (Phase 4): Detailed architecture documentation with diagrams.
