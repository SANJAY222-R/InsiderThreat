import sys
from pathlib import Path

# Ensure modules are in path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from config import logger, get_raw_csv_files
from modules.loader import DatasetLoader
from modules.validation import DataValidation
from modules.duplicates import DuplicateRemoval
from modules.missing import MissingValueHandler
from modules.timestamps import TimestampStandardizer
from modules.text import TextNormalizer
from modules.types import TypeStandardizer
from modules.session_prep import SessionPreparator
from modules.consistency import ConsistencyChecker
from modules.logging_engine import PreprocessingLogger
from modules.export import DataExporter
from modules.reporting import ReportGenerator

def main() -> None:
    logger.info("Starting Enterprise Data Cleaning and Preprocessing Pipeline (Phase 2)")
    
    files = get_raw_csv_files()
    
    loader = DatasetLoader()
    validator = DataValidation()
    dupe_remover = DuplicateRemoval()
    missing_handler = MissingValueHandler()
    timestamp_std = TimestampStandardizer()
    text_norm = TextNormalizer()
    type_std = TypeStandardizer()
    session_prep = SessionPreparator()
    consistency = ConsistencyChecker()
    exporter = DataExporter()
    
    log_engine = PreprocessingLogger()
    reporter = ReportGenerator()
    
    for file in files:
        try:
            log_engine.log_start(file.name)
            context = {"filename": file.name}
            
            # Module 1
            df = loader.load(file)
            
            # Modules 2-9
            df = validator.run(df, context)
            df = dupe_remover.run(df, context)
            df = missing_handler.run(df, context)
            df = timestamp_std.run(df, context)
            df = text_norm.run(df, context)
            df = consistency.run(df, context)
            df = type_std.run(df, context)
            df = session_prep.run(df, context)
            
            # Module 11
            df = exporter.run(df, context)
            
            # Module 10
            log_engine.log_end(df, context)
            
        except Exception as e:
            logger.error(f"Failed processing {file.name}: {e}", exc_info=True)
            
    # Module 12
    reporter.generate(log_engine.get_logs())
    logger.info("Phase 2 Pipeline Execution Completed.")

if __name__ == "__main__":
    main()
