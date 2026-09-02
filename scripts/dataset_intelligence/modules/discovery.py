import os
import pandas as pd
import polars as pl
from pathlib import Path
from config import get_csv_files, REPORTS_DIR, logger

class DatasetDiscovery:
    def __init__(self):
        self.files = get_csv_files()
        
    def get_line_count(self, file_path):
        try:
            # Polars is extremely fast at getting the row count
            return pl.scan_csv(file_path).select(pl.len()).collect().item()
        except Exception as e:
            logger.warning(f"Polars failed to count lines for {file_path}, falling back to chunking: {e}")
            count = 0
            for chunk in pd.read_csv(file_path, chunksize=1000000, low_memory=False, usecols=[0]):
                count += len(chunk)
            return count

    def get_col_count(self, file_path):
        try:
            df = pd.read_csv(file_path, nrows=0)
            return len(df.columns)
        except Exception:
            return 0

    def run(self):
        logger.info("Module 1: Automatic Dataset Discovery")
        inventory = []
        
        for file in self.files:
            logger.info(f"Discovering {file.name}...")
            size_bytes = file.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            try:
                num_records = self.get_line_count(file)
                num_cols = self.get_col_count(file)
            except Exception as e:
                logger.error(f"Failed to process {file.name}: {e}")
                num_records = 0
                num_cols = 0
            
            # Estimate processing time (rough heuristic based on size)
            estimated_time = f"{max(1, int(size_mb / 100))} seconds"
            
            inventory.append({
                "Filename": file.name,
                "Absolute Path": str(file.resolve()),
                "Extension": file.suffix,
                "Encoding": "utf-8", # Assumed default, checking strictly is expensive
                "Separator": ",",
                "Compression": "None",
                "Number of Records": num_records,
                "Number of Columns": num_cols,
                "Disk Size (MB)": round(size_mb, 2),
                "Memory Usage Estimate (MB)": round(size_mb * 1.5, 2), # pandas overhead
                "Estimated Processing Time": estimated_time
            })
            
        df = pd.DataFrame(inventory)
        df.to_csv(REPORTS_DIR / "dataset_inventory.csv", index=False)
        logger.info(f"Inventory saved. Found {len(df)} files.")
        return df
