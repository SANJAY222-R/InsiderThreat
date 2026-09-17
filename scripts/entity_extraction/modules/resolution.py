from typing import Any, Dict
import polars as pl
from .base_extractor import BaseEntityModule
import logging
import uuid

logger = logging.getLogger("EntityExtraction")

class EntityResolver(BaseEntityModule):
    """Module 3: Entity Resolution"""

    def run(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        prefix_map = {
            "users": "ENT-USR",
            "hosts": "ENT-HST",
            "files": "ENT-FIL",
            "usbs": "ENT-USB",
            "emails": "ENT-EML",
            "domains": "ENT-DOM",
            "websites": "ENT-WEB",
            "urls": "ENT-URL",
            "departments": "ENT-DPT",
            "sessions": "ENT-SES"
        }
        
        for k, df in entities.items():
            if df.is_empty():
                df = df.with_columns(pl.lit("").cast(pl.Utf8).alias("enterprise_id"))
                entities[k] = df
                continue
                
            # Exact match deduplication based on standard_id
            df = df.unique(subset=["standard_id"])
            
            # Generate deterministic enterprise IDs based on row index or hash, here we'll use a sequential ID for simplicity and speed
            prefix = prefix_map.get(k, "ENT-UNK")
            
            # Use row numbers to generate unique IDs
            df = df.with_row_index("id_num")
            df = df.with_columns(
                pl.concat_str([
                    pl.lit(prefix + "-"), 
                    (pl.col("id_num") + 1).cast(pl.Utf8).str.pad_start(6, '0')
                ]).alias("enterprise_id")
            ).drop("id_num")
            
            entities[k] = df
            logger.info(f"Resolved {df.height} unique entities for {k}.")
            
        return entities
