import polars as pl
from pathlib import Path
import logging

logger = logging.getLogger("DatasetPreprocessing")

class DatasetLoader:
    """Module 1: Automatic Dataset Discovery and Loading"""
    
    def load(self, file_path: Path) -> pl.DataFrame:
        logger.info(f"Loading {file_path.name}...")
        try:
            # Using Polars for extremely fast CSV loading and parsing
            # For memory safety, we limit to 250k rows for extremely large files like http.csv
            df = pl.read_csv(file_path, ignore_errors=True, infer_schema_length=10000, n_rows=250000)
            logger.info(f"Loaded {df.height} records from {file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Failed to load {file_path.name}: {e}")
            raise
