import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class AttributeExtractor(BaseEntityModule):
    """Module 4: Entity Attribute Extraction"""
    
    def run(self, entities: dict) -> dict:
        if "users" not in entities or entities["users"].is_empty():
            return entities
            
        users_df = entities["users"]
        
        # All Phase 3 features were aggregated at the user level, so we join them to users
        feature_names = ["user", "file", "usb", "email", "web", "temporal", "session", "statistical", "risk_indicators"]
        
        for fname in feature_names:
            # risk_indicators doesn't have "_features" suffix in file name, but load_features might expect it or not
            # In base_extractor.py: load_features reads f"{name}_features.csv"
            # let's try reading it. If not found, try the raw name.
            ff = self.load_features(fname)
            if ff is None and fname == "risk_indicators":
                # Fallback for risk indicators
                import os
                path = os.path.join(self.features_dir, "risk_indicators.csv")
                if os.path.exists(path):
                    ff = pl.read_csv(path, ignore_errors=True)
                    
            if ff is not None and "user" in ff.columns:
                ff = ff.with_columns(pl.col("user").cast(pl.Utf8))
                # avoid duplicate columns if joining multiple times
                join_cols = [c for c in ff.columns if c != "user" and c not in users_df.columns]
                ff_sub = ff.select(["user"] + join_cols)
                users_df = users_df.join(ff_sub, left_on="raw_id", right_on="user", how="left")
                
        entities["users"] = users_df
            
        logger.info("Entity Attributes Extracted and Mapped.")
        return entities
