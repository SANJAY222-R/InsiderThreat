import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger("FeatureEngineering")

class FeatureDocumenter:
    """Module 13: Feature Documentation"""
    
    def __init__(self, cfg):
        self.metadata_dir = Path(cfg.paths.metadata_dir)
        
    def run(self, feature_sets: dict):
        logger.info("Generating Feature Catalog...")
        
        catalog = []
        
        for name, df in feature_sets.items():
            for col, dtype in zip(df.columns, df.dtypes):
                if col == "user":
                    continue
                    
                catalog.append({
                    "Feature Name": col,
                    "Source Module": name,
                    "Data Type": str(dtype),
                    "Future Graph Usage": "Node Feature" if name != "session_features" else "Edge/Node Feature"
                })
                
        catalog_df = pd.DataFrame(catalog)
        
        try:
            catalog_df.to_csv(self.metadata_dir / "feature_catalog.csv", index=False)
            
            with open(self.metadata_dir / "feature_catalog.md", "w") as f:
                f.write("# Enterprise Feature Catalog\n\n")
                f.write(catalog_df.to_markdown(index=False))
                f.write("\n")
                
            logger.info("Feature Catalog generated successfully.")
        except Exception as e:
            logger.error(f"Failed to generate documentation: {e}")
