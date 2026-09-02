import json
import yaml
from .base_extractor import BaseEntityModule
import logging
import os
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

logger = logging.getLogger("EntityExtraction")

class AttributeDef(BaseModel):
    name: str
    type: str
    description: str

class RelationshipDef(BaseModel):
    source: str
    target: str
    relation: str
    cardinality: str

class EntityDef(BaseModel):
    type: str
    description: str
    attributes: List[AttributeDef]
    logical_relationships: List[RelationshipDef]

class KnowledgeModel(BaseModel):
    version: str = "1.0"
    entities: List[EntityDef]

class KnowledgeModelGenerator(BaseEntityModule):
    """Module 6: Knowledge Model Generation"""
    
    def run(self):
        km = KnowledgeModel(
            entities=[
                EntityDef(
                    type="User",
                    description="Enterprise employee or contractor",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID"),
                        AttributeDef(name="raw_id", type="string", description="Original ID from raw logs"),
                        AttributeDef(name="standard_id", type="string", description="Cleaned ID")
                    ],
                    logical_relationships=[
                        RelationshipDef(source="User", target="Host", relation="LOGS_ON", cardinality="1:N"),
                        RelationshipDef(source="User", target="File", relation="ACCESSES", cardinality="1:N"),
                        RelationshipDef(source="User", target="Email", relation="SENDS", cardinality="1:N")
                    ]
                ),
                EntityDef(
                    type="Host",
                    description="Enterprise workstation or server",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID"),
                        AttributeDef(name="raw_id", type="string", description="Original PC name")
                    ],
                    logical_relationships=[
                        RelationshipDef(source="Host", target="USB", relation="CONNECTS", cardinality="1:N")
                    ]
                ),
                EntityDef(
                    type="File",
                    description="Enterprise file or document",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID"),
                        AttributeDef(name="raw_id", type="string", description="Original filename")
                    ],
                    logical_relationships=[]
                ),
                EntityDef(
                    type="USB",
                    description="Removable media device",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID")
                    ],
                    logical_relationships=[]
                ),
                EntityDef(
                    type="Email",
                    description="Email address inside or outside enterprise",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID"),
                        AttributeDef(name="domain", type="string", description="Extracted domain")
                    ],
                    logical_relationships=[
                        RelationshipDef(source="Email", target="Domain", relation="BELONGS_TO", cardinality="N:1")
                    ]
                ),
                EntityDef(
                    type="Domain",
                    description="Network domain extracted from URLs or emails",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID")
                    ],
                    logical_relationships=[]
                ),
                EntityDef(
                    type="Website",
                    description="Web URL accessed via HTTP",
                    attributes=[
                        AttributeDef(name="enterprise_id", type="string", description="Unique global ID")
                    ],
                    logical_relationships=[]
                )
            ]
        )
        
        json_path = os.path.join(self.cfg.paths.schemas_dir, "knowledge_model.json")
        yaml_path = os.path.join(self.cfg.paths.schemas_dir, "knowledge_model.yaml")
        
        with open(json_path, "w") as f:
            f.write(km.model_dump_json(indent=2))
            
        with open(yaml_path, "w") as f:
            yaml.dump(km.model_dump(), f, sort_keys=False)
            
        logger.info("Knowledge Model Generated and Exported.")
