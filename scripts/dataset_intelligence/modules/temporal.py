import polars as pl
import pandas as pd
from config import REPORTS_DIR, logger

class TemporalAnalysis:
    def run(self, inventory_df):
        logger.info("Module 7: Temporal Analysis")
        
        temporal_stats = []
        
        for _, row in inventory_df.iterrows():
            filepath = row["Absolute Path"]
            filename = row["Filename"]
            
            try:
                lf = pl.scan_csv(filepath)
                if row["Number of Records"] > 1_000_000:
                    lf = lf.head(1000000)
                columns = lf.columns
                date_col = "date" if "date" in columns else ("time" if "time" in columns else None)
                
                if date_col:
                    logger.info(f"Extracting temporal stats for {filename} using {date_col}")
                    
                    # Instead of parsing everything (expensive), let's get min/max via string sorting
                    # CERT dates are often MM/DD/YYYY HH:MM:SS which doesn't sort lexicographically well,
                    # but we will try to parse just the min/max or do a quick pass
                    
                    # For quick analysis without crashing on 14GB, we will sample or just get min/max
                    # Polars can parse dates: strptime
                    try:
                        parsed = lf.select(
                            pl.col(date_col).str.strptime(pl.Datetime, "%m/%d/%Y %H:%M:%S", strict=False)
                        )
                        stats = parsed.select([
                            pl.col(date_col).min().alias("First Event"),
                            pl.col(date_col).max().alias("Last Event")
                        ]).collect().to_dicts()[0]
                        
                        temporal_stats.append({
                            "Dataset": filename,
                            "First Event": stats["First Event"],
                            "Last Event": stats["Last Event"]
                        })
                    except Exception as e:
                        logger.warning(f"Could not parse dates in {filename}: {e}")
                        
            except Exception as e:
                logger.error(f"Error in temporal analysis for {filename}: {e}")
                
        df = pd.DataFrame(temporal_stats)
        df.to_csv(REPORTS_DIR / "temporal_summary.csv", index=False)
        logger.info("Temporal analysis completed.")
