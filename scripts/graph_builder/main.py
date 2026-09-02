# Update main.py imports to match combined file
import os
import sys
import logging
from pathlib import Path
from omegaconf import OmegaConf
import networkx as nx

# Ensure modules are in path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from modules.node_creation import NodeCreator
from modules.edge_creation import EdgeCreator
from modules.temporal_snapshots_features import TemporalModeler, SnapshotGenerator, NodeFeatureAttacher, EdgeFeatureAttacher
from modules.schema_validation_analytics import SchemaGenerator, GraphValidator, GraphAnalytics
from modules.export_visualize_report import GraphExporter, GraphVisualizer, ReportGenerator

logger = logging.getLogger("GraphBuilder")
logger.setLevel(logging.INFO)

def setup_directories(cfg):
    dirs = [
        cfg.paths.nodes_dir, cfg.paths.edges_dir, cfg.paths.snapshots_dir,
        cfg.paths.analytics_dir, cfg.paths.validation_dir, cfg.paths.exporters_dir,
        cfg.paths.visualizations_dir, cfg.paths.schemas_dir, cfg.paths.reports_dir,
        cfg.paths.logs_dir
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def main():
    cfg = OmegaConf.load(BASE_DIR / "conf" / "config.yaml")
    setup_directories(cfg)
    
    # Configure logging
    fh = logging.FileHandler(Path(cfg.paths.logs_dir) / "graph_builder.log")
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    logger.info("Starting Phase 5: Temporal Heterogeneous Graph Construction Framework")
    
    G = nx.MultiDiGraph()
    
    if cfg.modules.node_creation:
        logger.info("Module 1: Node Creation")
        G = NodeCreator(cfg).run(G)
        
    if cfg.modules.edge_creation:
        logger.info("Module 2: Edge Creation")
        G = EdgeCreator(cfg).run(G)
        
    if cfg.modules.temporal_modeling:
        logger.info("Module 3: Temporal Modeling")
        G = TemporalModeler(cfg).run(G)
        
    if cfg.modules.snapshots:
        logger.info("Module 4: Graph Snapshots")
        SnapshotGenerator(cfg).run(G)
        
    if cfg.modules.node_features:
        logger.info("Module 5: Node Features")
        G = NodeFeatureAttacher(cfg).run(G)
        
    if cfg.modules.edge_features:
        logger.info("Module 6: Edge Features")
        G = EdgeFeatureAttacher(cfg).run(G)
        
    if cfg.modules.schema_generation:
        logger.info("Module 7: Graph Schema")
        SchemaGenerator(cfg).run(G)
        
    if cfg.modules.validation:
        logger.info("Module 8: Graph Validation")
        GraphValidator(cfg).run(G)
        
    if cfg.modules.analytics:
        logger.info("Module 9: Graph Analytics")
        GraphAnalytics(cfg).run(G)
        
    if cfg.modules.storage_export:
        logger.info("Module 10: Graph Storage Export")
        GraphExporter(cfg).run(G)
        
    if cfg.modules.visualization:
        logger.info("Module 11: Graph Visualization")
        GraphVisualizer(cfg).run(G)
        
    if cfg.modules.reporting:
        logger.info("Module 12: Report Generation")
        ReportGenerator(cfg).run(G)
        
    logger.info("Phase 5 Execution Completed.")

if __name__ == "__main__":
    main()
