from typing import Any, Dict
import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class EntityStandardizer(BaseEntityModule):
    """Module 2: Entity Standardization"""

    def run(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        for k, df in entities.items():
            if df.is_empty():
                continue
                
            # Standardize string casing
            df = df.with_columns(
                pl.col("raw_id").cast(pl.Utf8).str.strip_chars().alias("raw_id")
            )
            
            if k == "emails":
                df = df.with_columns(pl.col("raw_id").str.to_lowercase().alias("standard_id"))
                # Extract domain
                df = df.with_columns(
                    pl.col("standard_id").str.split("@").list.get(1).alias("domain")
                )
                
                # Add domains to the domains entity list if they don't exist
                domains = df.drop_nulls("domain").select(pl.col("domain").alias("raw_id")).unique()
                if not domains.is_empty():
                    entities["domains"] = pl.concat([entities["domains"], domains]).unique()
                    
            elif k == "urls" or k == "websites":
                df = df.with_columns(pl.col("raw_id").str.to_lowercase().alias("standard_id"))
                
            elif k == "files":
                # Ensure backslashes are uniform or paths are clean
                df = df.with_columns(pl.col("raw_id").str.replace_all(r"\\\\", "/").alias("standard_id"))
                
            else:
                # Default standardization
                df = df.with_columns(pl.col("raw_id").alias("standard_id"))
                
            entities[k] = df
            
        logger.info("Entity Standardization Complete.")
        return entities
