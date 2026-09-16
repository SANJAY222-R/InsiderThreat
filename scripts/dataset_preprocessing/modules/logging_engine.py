import time
from typing import Any
import psutil
import polars as pl
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class PreprocessingLogger:
    """Module 10: Preprocessing Logging Engine"""
    
    def __init__(self) -> None:
        self.logs: list[dict[str, Any]] = []
        self.current: dict[str, Any] = {}
        
    def log_start(self, filename: str) -> None:
        self.current = {
            "Filename": filename,
            "Start Time": time.time(),
            "Memory Start (MB)": psutil.Process().memory_info().rss / (1024 * 1024)
        }
        
    def log_end(self, df: pl.DataFrame | None, context: dict[str, Any]) -> None:
        self.current["End Time"] = time.time()
        self.current["Duration (s)"] = round(self.current["End Time"] - self.current["Start Time"], 2)
        self.current["Memory End (MB)"] = psutil.Process().memory_info().rss / (1024 * 1024)
        self.current["Final Rows"] = df.height if df is not None else 0
        self.current["Context"] = context
        self.logs.append(self.current)
        logger.info(f"Finished processing {self.current['Filename']} in {self.current['Duration (s)']}s")
        
    def get_logs(self) -> list[dict[str, Any]]:
        return self.logs
