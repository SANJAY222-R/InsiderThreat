import pandas as pd
from config import REPORTS_DIR
import logging

logger = logging.getLogger("DatasetPreprocessing")

class ReportGenerator:
    """Module 12: Report Generation"""
    
    def generate(self, logs: list):
        logger.info("Generating Preprocessing Reports...")
        
        # Flatten context
        flat_logs = []
        for log in logs:
            flat = {
                "Filename": log["Filename"],
                "Duration (s)": log["Duration (s)"],
                "Memory End (MB)": log["Memory End (MB)"],
                "Final Rows": log["Final Rows"]
            }
            context = log.get("Context", {})
            flat["Duplicates Removed"] = context.get("duplicates_removed", 0)
            flat["Validation Warnings"] = context.get("validation_warnings", "")
            flat["Consistency Issues"] = len(context.get("consistency_issues", []))
            flat_logs.append(flat)
            
        df = pd.DataFrame(flat_logs)
        
        # CSV
        df.to_csv(REPORTS_DIR / "preprocessing_summary.csv", index=False)
        
        # Markdown
        with open(REPORTS_DIR / "preprocessing_report.md", "w") as f:
            f.write("# Enterprise Data Preprocessing Report\n\n")
            f.write("## Execution Statistics\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")
            
        # HTML
        df.to_html(REPORTS_DIR / "preprocessing_report.html", index=False)
        
        logger.info("Reports generated successfully.")
