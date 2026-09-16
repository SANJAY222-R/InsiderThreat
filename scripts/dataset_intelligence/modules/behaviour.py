import polars as pl
import pandas as pd
from config import REPORTS_DIR, logger

class BehaviourProfiler:
    def run(self, inventory_df: pd.DataFrame) -> None:
        logger.info("Module 8: User Behaviour Profiling")
        
        user_profiles = {}
        
        for _, row in inventory_df.iterrows():
            filepath = row["Absolute Path"]
            filename = row["Filename"]
            
            try:
                lf = pl.scan_csv(filepath)
                if row["Number of Records"] > 1_000_000:
                    lf = lf.head(1000000)
                if "user" not in lf.columns:
                    continue
                    
                logger.info(f"Aggregating user behaviour in {filename}")
                
                # Count events per user
                user_counts = lf.group_by("user").len().collect()
                
                for r in user_counts.iter_rows(named=True):
                    user = r["user"]
                    if user not in user_profiles:
                        user_profiles[user] = {"Total Events": 0}
                    user_profiles[user]["Total Events"] += r["len"]
                    user_profiles[user][f"{filename} Events"] = r["len"]
                    
            except Exception as e:
                logger.error(f"Error profiling behaviour in {filename}: {e}")
                
        if user_profiles:
            df = pd.DataFrame.from_dict(user_profiles, orient="index").reset_index()
            df = df.rename(columns={"index": "User"})
            df.fillna(0, inplace=True)
            df.to_csv(REPORTS_DIR / "behaviour_profiles.csv", index=False)
            logger.info("Behaviour profiling completed.")
