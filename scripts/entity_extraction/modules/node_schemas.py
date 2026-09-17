import json
from .base_extractor import BaseEntityModule
import logging
import os
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

logger = logging.getLogger("EntityExtraction")

class NodeSchema(BaseModel):
    node_id: str = Field(description="Unique Enterprise ID mapping to the node")
    entity_type: str = Field(description="Type of the entity (e.g., User, Host)")
    attributes: Dict[str, Any] = Field(description="Dictionary of string or numeric attributes")
    feature_vector_ref: Optional[str] = Field(description="Reference to a row in feature matrices")
    metadata: Dict[str, Any] = Field(description="Creation tracking metadata")

class GraphNodeSchemaDoc(BaseModel):
    version: str = "1.0"
    schema_definition: Dict[str, Any]

class NodeSchemaGenerator(BaseEntityModule):
    """Module 7: Node Schema Generation"""

    def run(self) -> None:
        doc = GraphNodeSchemaDoc(
            schema_definition=NodeSchema.model_json_schema()
        )
        
        path = os.path.join(self.cfg.paths.schemas_dir, "node_schema.json")
        with open(path, "w") as f:
            f.write(doc.model_dump_json(indent=2))
            
        logger.info("Node Schema Generated.")
