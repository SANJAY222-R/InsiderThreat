import pandas as pd
from config import REPORTS_DIR, logger

class SummaryGenerator:
    def run(self, inventory_df: pd.DataFrame, schema_df: pd.DataFrame, profiling_stats: dict[str, pd.DataFrame]) -> None:
        logger.info("Module 11 & 12: Dataset Summary and Recommendations")
        
        total_records = inventory_df["Number of Records"].sum()
        total_size = inventory_df["Disk Size (MB)"].sum()
        
        with open(REPORTS_DIR / "dataset_summary.md", "w") as f:
            f.write("# Dataset Summary\n\n")
            f.write(f"- Total Files: {len(inventory_df)}\n")
            f.write(f"- Total Records: {total_records:,}\n")
            f.write(f"- Total Size: {total_size:,.2f} MB\n")
            
        with open(REPORTS_DIR / "phase2_recommendations.md", "w") as f:
            f.write("# Phase 2 Recommendations\n\n")
            f.write("## Data Cleaning\n")
            f.write("- Standardize all timestamps to UTC/ISO format.\n")
            f.write("- Handle any NULL values identified in the profiling step.\n\n")
            f.write("## Feature Engineering\n")
            f.write("- Convert categorical identifiers (like user, pc) into categorical integer codes.\n")
            f.write("- Extract hour of day and day of week from timestamps.\n\n")
            f.write("## Graph Generation\n")
            f.write("- `user` and `pc` are strong node candidates.\n")
            f.write("- Edges should be generated based on event co-occurrences.\n")
            
        logger.info("Summary and recommendations generated.")
