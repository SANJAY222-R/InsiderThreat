import pandas as pd
import plotly.express as px
from config import VIZ_DIR, logger

class DataVisualizer:
    def run(self, inventory_df: pd.DataFrame, profiling_stats: dict[str, pd.DataFrame]) -> None:
        logger.info("Module 10: Visualization")
        
        try:
            # Dataset Size Comparison
            fig = px.bar(inventory_df, x="Filename", y="Disk Size (MB)", title="Dataset File Sizes")
            fig.write_html(VIZ_DIR / "dataset_sizes.html")
            
            # Record Count Comparison
            fig2 = px.pie(inventory_df, names="Filename", values="Number of Records", title="Record Distribution")
            fig2.write_html(VIZ_DIR / "record_distribution.html")
            
            logger.info("Visualizations generated successfully.")
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
