import time
import psutil
from .base_module import BaseModule
import logging

logger = logging.getLogger("DatasetPreprocessing")

class PreprocessingLogger:
    """Module 10: Preprocessing Logging Engine"""
    
    def __init__(self):
        self.logs = []
        
    def log_start(self, filename: str):
        self.current = {
            "Filename": filename,
            "Start Time": time.time(),
            "Memory Start (MB)": psutil.Process().memory_info().rss / (1024 * 1024)
        }
        
    def log_end(self, df, context):
        self.current["End Time"] = time.time()
        self.current["Duration (s)"] = round(self.current["End Time"] - self.current["Start Time"], 2)
        self.current["Memory End (MB)"] = psutil.Process().memory_info().rss / (1024 * 1024)
        self.current["Final Rows"] = df.height if df is not None else 0
        self.current["Context"] = context
        self.logs.append(self.current)
        logger.info(f"Finished processing {self.current['Filename']} in {self.current['Duration (s)']}s")
        
    def get_logs(self):
        return self.logs
