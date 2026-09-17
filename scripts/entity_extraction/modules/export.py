import os
from typing import Any, Dict
import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class EntityExporter(BaseEntityModule):
    """Module 11: Entity Export"""

    def run(self, entities: Dict[str, Any]) -> None:
        for k, df in entities.items():
            if df.is_empty():
                continue
                
            path = os.path.join(self.cfg.paths.entities_dir, f"{k}.csv")
            df.write_csv(path)
            logger.info(f"Exported {k} to {path}")
            
        logger.info("Entity Export Completed.")
