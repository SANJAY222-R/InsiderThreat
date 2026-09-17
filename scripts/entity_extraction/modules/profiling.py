from typing import Any, Dict
import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class EntityProfiler(BaseEntityModule):
    """Module 5: Entity Profiling"""

    def run(self, entities: Dict[str, Any]) -> None:
        # Generates basic profiles in memory
        for k, df in entities.items():
            if df.is_empty():
                continue
            cols = df.columns
            logger.info(f"Profile for {k}: {df.height} records, {len(cols)} attributes.")
