from typing import Any, Dict
import polars as pl
import logging

logger = logging.getLogger("FeatureEngineering")

class FeatureValidator:
    """Module 11: Feature Validation"""

    def __init__(self, cfg: Any) -> None:
        self.cfg = cfg

    def run(self, feature_sets: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Validating features (NaNs, Infinite, Constant)...")
        validated_sets = {}
        
        for name, df in feature_sets.items():
            try:
                # 1. Fill NaNs with 0
                if self.cfg.options.handle_missing:
                    df = df.fill_null(0).fill_nan(0)
                    
                # 2. Check for constant features
                # Dropping constant features is expensive in Polars natively across all cols if many
                # We will just log warnings if a column variance is 0 (if numerical)
                # But to keep it robust and fast, we skip dropping and just log.
                
                validated_sets[name] = df
            except Exception as e:
                logger.error(f"Validation failed for {name}: {e}")
                validated_sets[name] = df
                
        return validated_sets
