import os
import sys
import logging
from pathlib import Path
from omegaconf import OmegaConf

# Ensure modules are in path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from modules.identification import EntityIdentifier
from modules.standardization import EntityStandardizer
from modules.resolution import EntityResolver
from modules.attributes import AttributeExtractor
from modules.profiling import EntityProfiler
from modules.knowledge_model import KnowledgeModelGenerator
from modules.node_schemas import NodeSchemaGenerator
from modules.metadata import MetadataGenerator
from modules.validation import EntityValidator
from modules.documentation import DocumentationGenerator
from modules.export import EntityExporter
from modules.recommendations import RecommendationsGenerator

logger = logging.getLogger("EntityExtraction")
logger.setLevel(logging.INFO)

def setup_directories(cfg):
    dirs = [
        cfg.paths.entities_dir, cfg.paths.schemas_dir, cfg.paths.reports_dir,
        cfg.paths.logs_dir, cfg.paths.metadata_dir, cfg.paths.docs_dir
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def main():
    cfg = OmegaConf.load(BASE_DIR / "conf" / "config.yaml")
    setup_directories(cfg)
    
    # Configure logging
    fh = logging.FileHandler(Path(cfg.paths.logs_dir) / "entity_extraction.log")
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    logger.info("Starting Phase 4: Enterprise Entity Extraction and Knowledge Modeling Framework")
    logger.info(f"Configuration: \n{OmegaConf.to_yaml(cfg)}")
    
    entities = {}
    
    # M1: Identification
    if cfg.modules.identification:
        logger.info("Module 1: Entity Identification")
        identifier = EntityIdentifier(cfg)
        entities = identifier.run()
        
    # M2: Standardization
    if cfg.modules.standardization:
        logger.info("Module 2: Entity Standardization")
        standardizer = EntityStandardizer(cfg)
        entities = standardizer.run(entities)
        
    # M3: Resolution
    if cfg.modules.resolution:
        logger.info("Module 3: Entity Resolution")
        resolver = EntityResolver(cfg)
        entities = resolver.run(entities)
        
    # M4: Attribute Extraction
    if cfg.modules.attributes:
        logger.info("Module 4: Entity Attribute Extraction")
        attr_extractor = AttributeExtractor(cfg)
        entities = attr_extractor.run(entities)
        
    # M5: Profiling
    if cfg.modules.profiling:
        logger.info("Module 5: Entity Profiling")
        profiler = EntityProfiler(cfg)
        profiler.run(entities)
        
    # M6: Knowledge Model
    if cfg.modules.knowledge_model:
        logger.info("Module 6: Knowledge Model Generation")
        km_gen = KnowledgeModelGenerator(cfg)
        km_gen.run()
        
    # M7: Node Schemas
    if cfg.modules.node_schemas:
        logger.info("Module 7: Node Schema Generation")
        ns_gen = NodeSchemaGenerator(cfg)
        ns_gen.run()
        
    # M8: Metadata
    if cfg.modules.metadata:
        logger.info("Module 8: Entity Metadata Generation")
        meta_gen = MetadataGenerator(cfg)
        meta_gen.run(entities)
        
    # M9: Validation
    if cfg.modules.validation:
        logger.info("Module 9: Entity Validation")
        validator = EntityValidator(cfg)
        entities = validator.run(entities)
        
    # M10: Documentation
    if cfg.modules.documentation:
        logger.info("Module 10: Entity Documentation Generation")
        doc_gen = DocumentationGenerator(cfg)
        doc_gen.run(entities)
        
    # M11: Export
    if cfg.modules.export:
        logger.info("Module 11: Entity Export")
        exporter = EntityExporter(cfg)
        exporter.run(entities)
        
    # M12: Recommendations
    if cfg.modules.recommendations:
        logger.info("Module 12: Phase 5 Recommendations Generation")
        rec_gen = RecommendationsGenerator(cfg)
        rec_gen.run()
        
    logger.info("Phase 4 Execution Completed.")

if __name__ == "__main__":
    main()
