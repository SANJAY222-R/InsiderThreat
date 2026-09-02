import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class EntityValidator(BaseEntityModule):
    """Module 9: Entity Validation"""
    
    def run(self, entities: dict) -> dict:
        for k, df in entities.items():
            if df.is_empty():
                continue
            
            # Check missing standard IDs
            if "standard_id" in df.columns:
                null_count = df.select(pl.col("standard_id").is_null().sum()).item()
                if null_count > 0:
                    logger.warning(f"Entity '{k}' has {null_count} missing standard_ids.")
                    
            # Check missing enterprise IDs
            if "enterprise_id" in df.columns:
                null_count = df.select(pl.col("enterprise_id").is_null().sum()).item()
                if null_count > 0:
                    logger.warning(f"Entity '{k}' has {null_count} missing enterprise_ids.")
                    
        logger.info("Entity Validation Completed.")
        return entities
