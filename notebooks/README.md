# Jupyter Notebooks

## Available Notebooks

| Notebook | Phase | Purpose |
|----------|-------|---------|
| `01_data_exploration.ipynb` | Phase 1 | Explore CERT r4.2 dataset |
| `02_graph_analysis.ipynb` | Phase 3 | Graph construction & analysis |
| `03_model_experiments.ipynb` | Phase 4-5 | THGNN experiments |

## Setup

```bash
pip install jupyter ipykernel
python -m ipykernel install --user --name insider-threat
jupyter lab
```

## Guidelines

- Use notebooks for exploration and prototyping ONLY
- Move production code to the appropriate module
- Clear outputs before committing
- Add markdown cells explaining analysis steps
