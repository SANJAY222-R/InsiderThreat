from typing import Any
import os
import sys
import logging
from pathlib import Path
import hydra
from omegaconf import DictConfig, OmegaConf

# Ensure modules are in path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from modules.user_behavior import UserBehaviorExtractor
from modules.file_activity import FileActivityExtractor
from modules.usb_activity import UsbActivityExtractor
from modules.email_activity import EmailActivityExtractor
from modules.web_activity import WebActivityExtractor
from modules.temporal import TemporalExtractor
from modules.sessions import SessionExtractor
from modules.statistics import StatisticsExtractor
from modules.risk_indicators import RiskIndicatorExtractor
from modules.normalization import FeatureNormalizer
from modules.validation import FeatureValidator
from modules.export import FeatureExporter
from modules.documentation import FeatureDocumenter
from modules.reporting import FeatureReporter

logger = logging.getLogger("FeatureEngineering")
logger.setLevel(logging.INFO)

def setup_directories(cfg: Any) -> None:
    for d in [cfg.paths.features_dir, cfg.paths.reports_dir, cfg.paths.logs_dir, cfg.paths.metadata_dir]:
        Path(d).mkdir(parents=True, exist_ok=True)

def main() -> None:
    cfg = OmegaConf.load(BASE_DIR / "conf" / "config.yaml")
    setup_directories(cfg)
    
    # Configure logging
    fh = logging.FileHandler(Path(cfg.paths.logs_dir) / "feature_engineering.log")
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    logger.info("Starting Phase 3: Enterprise Feature Engineering Framework")
    logger.info(f"Configuration: \n{OmegaConf.to_yaml(cfg)}")
    
    # Initialize all modules
    extractors = []
    if cfg.features.user_behavior: extractors.append(UserBehaviorExtractor(cfg))
    if cfg.features.file_activity: extractors.append(FileActivityExtractor(cfg))
    if cfg.features.usb_activity: extractors.append(UsbActivityExtractor(cfg))
    if cfg.features.email_activity: extractors.append(EmailActivityExtractor(cfg))
    if cfg.features.web_activity: extractors.append(WebActivityExtractor(cfg))
    if cfg.features.temporal: extractors.append(TemporalExtractor(cfg))
    if cfg.features.sessions: extractors.append(SessionExtractor(cfg))
    if cfg.features.statistics: extractors.append(StatisticsExtractor(cfg))
    if cfg.features.risk_indicators: extractors.append(RiskIndicatorExtractor(cfg))
    
    validator = FeatureValidator(cfg)
    normalizer = FeatureNormalizer(cfg)
    exporter = FeatureExporter(cfg)
    documenter = FeatureDocumenter(cfg)
    reporter = FeatureReporter(cfg)
    
    feature_sets = {}
    
    # Extract features
    for extractor in extractors:
        logger.info(f"Running Extractor: {extractor.name}")
        try:
            feat_df = extractor.run()
            if feat_df is not None:
                feature_sets[extractor.name] = feat_df
        except Exception as e:
            logger.error(f"Failed in {extractor.name}: {e}", exc_info=True)
            
    # Validate features
    logger.info("Running Feature Validation (Module 11)")
    feature_sets = validator.run(feature_sets)
    
    # Normalize features
    logger.info("Running Feature Normalization (Module 10)")
    feature_sets = normalizer.run(feature_sets)
    
    # Export features
    logger.info("Exporting Features (Module 12)")
    exporter.run(feature_sets)
    
    # Documentation
    logger.info("Generating Documentation (Module 13)")
    documenter.run(feature_sets)
    
    # Reporting
    if cfg.options.generate_reports:
        logger.info("Generating Reports (Module 14)")
        reporter.run(feature_sets)
        
    logger.info("Phase 3 Execution Completed.")

if __name__ == "__main__":
    main()
