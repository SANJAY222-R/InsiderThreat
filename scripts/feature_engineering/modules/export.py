import polars as pl
import logging
from pathlib import Path

logger = logging.getLogger("FeatureEngineering")

class FeatureExporter:
    """Module 12: Feature Export"""
    
    def __init__(self, cfg):
        self.out_dir = Path(cfg.paths.features_dir)
        
    def run(self, feature_sets: dict):
        logger.info("Exporting feature sets to CSV...")
        
        for name, df in feature_sets.items():
            path = self.out_dir / f"{name}.csv"
            try:
                df.write_csv(path)
                logger.info(f"Exported {name} -> {path.name}")
            except Exception as e:
                logger.error(f"Failed exporting {name}: {e}")
                
        # Additionally, attempt to merge all user-keyed features into a unified user_features.csv
        try:
            logger.info("Attempting to generate unified user_features.csv...")
            unified_df = None
            for name, df in feature_sets.items():
                if "user" in df.columns:
                    if unified_df is None:
                        unified_df = df
                    else:
                        unified_df = unified_df.join(df, on="user", how="outer_coalesce")
            
            if unified_df is not None:
                unified_df = unified_df.fill_null(0).fill_nan(0)
                unified_df.write_csv(self.out_dir / "user_features.csv")
                logger.info("Exported unified user_features.csv successfully.")
        except Exception as e:
            logger.error(f"Failed to generate unified user_features: {e}", exc_info=True)
