import os
import logging
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if not (BASE_DIR / "dataset").exists():
    BASE_DIR = Path(r"C:\Users\HP\Desktop\InsiderThreat")

RAW_DIR = BASE_DIR / "dataset" / "raw"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"
METADATA_DIR = BASE_DIR / "metadata"
REPORTS_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories
for d in [PROCESSED_DIR, METADATA_DIR, REPORTS_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logger setup
logger = logging.getLogger("DatasetPreprocessing")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_DIR / "dataset_preprocessing.log")
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Prevent duplicate logs
if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)

def get_raw_csv_files():
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        logger.warning("No CSVs found in dataset/raw. Checking r4.2 fallback.")
        fallback = BASE_DIR / "r4.2"
        files = list(fallback.glob("*.csv"))
    return files
