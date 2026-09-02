import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger("FeatureEngineering")

class FeatureReporter:
    """Module 14: Feature Reports"""
    
    def __init__(self, cfg):
        self.reports_dir = Path(cfg.paths.reports_dir)
        
    def run(self, feature_sets: dict):
        logger.info("Generating Feature Reports (Statistics, Missing)...")
        
        try:
            with open(self.reports_dir / "feature_statistics.md", "w") as f:
                f.write("# Feature Engineering Statistical Report\n\n")
                
                for name, df in feature_sets.items():
                    pd_df = df.to_pandas()
                    f.write(f"## Module: {name}\n")
                    f.write(f"- Total Users/Entities: {len(pd_df)}\n")
                    f.write(f"- Total Features: {len(pd_df.columns) - 1}\n\n")
                    
                    f.write("### Basic Statistics\n")
                    f.write(pd_df.describe().to_markdown())
                    f.write("\n\n")
                    
            logger.info("Feature Reports generated successfully.")
        except Exception as e:
            logger.error(f"Failed to generate feature reports: {e}")
