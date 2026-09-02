import polars as pl
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import pandas as pd
import logging
import joblib
from pathlib import Path

logger = logging.getLogger("FeatureEngineering")

class FeatureNormalizer:
    """Module 10: Feature Normalization"""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.method = cfg.options.normalization_method
        self.metadata_dir = Path(cfg.paths.metadata_dir)
        
    def run(self, feature_sets: dict) -> dict:
        if self.method == "none":
            return feature_sets
            
        logger.info(f"Normalizing features using {self.method} scaling...")
        normalized_sets = {}
        
        for name, df in feature_sets.items():
            # Exclude non-numeric columns like 'user' from scaling
            numeric_cols = [c for c, t in zip(df.columns, df.dtypes) if t in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]]
            
            if not numeric_cols:
                normalized_sets[name] = df
                continue
                
            pd_df = df.to_pandas()
            
            if self.method == "minmax":
                scaler = MinMaxScaler()
            elif self.method == "robust":
                scaler = RobustScaler()
            else:
                scaler = StandardScaler()
                
            # Fit and transform
            try:
                pd_df[numeric_cols] = scaler.fit_transform(pd_df[numeric_cols])
                
                # Store scaler
                joblib.dump(scaler, self.metadata_dir / f"{name}_scaler.joblib")
                
                normalized_sets[name] = pl.from_pandas(pd_df)
            except Exception as e:
                logger.error(f"Failed to normalize {name}: {e}")
                normalized_sets[name] = df # Fallback to raw
                
        return normalized_sets
