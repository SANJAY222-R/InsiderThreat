# Data Flow Architecture

## Pipeline Overview

```
Raw Logs (CSV) → Preprocessing → Feature Engineering → Graph Builder
    ↓                                                       ↓
 Dataset/                                           HeteroData (PyG)
 processed/                                              ↓
                                                   THGNN Training
                                                        ↓
                                                  Model Checkpoint
                                                        ↓
                                              Inference Engine ← API Request
                                                        ↓
                                              Prediction + XAI → Dashboard
```

TODO: Detailed data flow diagrams for each pipeline stage.
