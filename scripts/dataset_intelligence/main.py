import sys
from pathlib import Path

# Ensure modules are in path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from config import logger
from modules.discovery import DatasetDiscovery
from modules.schema import SchemaDiscovery
from modules.profiler import DataProfiler
from modules.dictionary import DictionaryGenerator
from modules.entities import EntityDiscovery
from modules.temporal import TemporalAnalysis
from modules.behaviour import BehaviourProfiler
from modules.quality import QualityAnalysis
from modules.visualizer import DataVisualizer
from modules.summary import SummaryGenerator

def main() -> None:
    logger.info("Starting Dataset Intelligence Module - Phase 1")
    
    try:
        # Module 1: Automatic Dataset Discovery
        discovery = DatasetDiscovery()
        inventory_df = discovery.run()
        
        # Module 2: Schema Discovery
        schema = SchemaDiscovery()
        schema_df = schema.run(inventory_df)
        
        # Module 4: Data Profiling (run before dictionary to get stats)
        profiler = DataProfiler()
        profiling_stats = profiler.run(inventory_df)
        
        # Module 3: Data Dictionary
        dictionary = DictionaryGenerator()
        dictionary.run(schema_df, profiling_stats)
        
        # Module 5 & 6: Entity & Relationship Discovery
        entities = EntityDiscovery()
        entities.run(inventory_df)
        
        # Module 7: Temporal Analysis
        temporal = TemporalAnalysis()
        temporal.run(inventory_df)
        
        # Module 8: User Behaviour Profiling
        behaviour = BehaviourProfiler()
        behaviour.run(inventory_df)
        
        # Module 9: Data Quality Analysis
        quality = QualityAnalysis()
        quality.run(inventory_df)
        
        # Module 10: Visualization
        visualizer = DataVisualizer()
        visualizer.run(inventory_df, profiling_stats)
        
        # Module 11 & 12: Dataset Summary & Recommendations
        summary = SummaryGenerator()
        summary.run(inventory_df, schema_df, profiling_stats)
        
        logger.info("Dataset Intelligence Module execution completed successfully.")
        
    except Exception as e:
        logger.error(f"Fatal error during execution: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
