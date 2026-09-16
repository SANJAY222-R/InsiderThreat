import os
import logging
from pathlib import Path

# Paths
BASE_DIR = Path(os.getcwd())
if not (BASE_DIR / "dataset").exists():
    # Fallback to absolute if run from wrong directory
    BASE_DIR = Path(r"C:\Users\HP\Desktop\InsiderThreat")

RAW_DIR = BASE_DIR / "dataset" / "raw"
METADATA_DIR = BASE_DIR / "metadata"
REPORTS_DIR = BASE_DIR / "reports"
VIZ_DIR = BASE_DIR / "visualizations"
DICT_DIR = BASE_DIR / "dictionary"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories
for d in [METADATA_DIR, REPORTS_DIR, VIZ_DIR, DICT_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logger setup
logger = logging.getLogger("DatasetIntelligence")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_DIR / "dataset_intelligence.log")
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def get_csv_files() -> list[Path]:
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        # Fallback to r4.2 if symlink failed
        logger.warning("No CSVs found in dataset/raw. Checking r4.2 fallback.")
        fallback = BASE_DIR / "r4.2"
        files = list(fallback.glob("*.csv"))
    return files
