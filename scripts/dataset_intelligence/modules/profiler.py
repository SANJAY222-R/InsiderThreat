import polars as pl
import pandas as pd
from config import REPORTS_DIR, logger

class DataProfiler:
    def run(self, inventory_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        logger.info("Module 4: Data Profiling")
        all_stats = {}
        
        for _, row in inventory_df.iterrows():
            filepath = row["Absolute Path"]
            filename = row["Filename"]
            logger.info(f"Profiling {filename}...")
            
            try:
                lf = pl.scan_csv(filepath)
                # Compute total records from inventory for efficiency
                total_records = row["Number of Records"]
                
                # Try to count exact duplicates if file is small enough, else skip
                if total_records < 5_000_000:
                    unique_rows = lf.unique().select(pl.len()).collect().item()
                    duplicate_records = total_records - unique_rows
                else:
                    duplicate_records = "Estimated (Too Large)"
                
                # Sample large files to prevent OOM / hanging (e.g., http.csv)
                if total_records > 1_000_000:
                    lf = lf.head(1000000)
                    
                # We will compute basic stats per column
                stats = []
                schema = lf.collect_schema()
                
                # Fetch a subset for heavy operations (like mode/median) to save memory/time
                # For basic ops like min/max/nulls we can run on the whole dataset lazily
                # We'll construct a lazy expression list
                exprs = []
                for col_name, dtype in schema.items():
                    exprs.extend([
                        pl.col(col_name).null_count().alias(f"{col_name}_nulls"),
                        pl.col(col_name).n_unique().alias(f"{col_name}_unique")
                    ])
                    if dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
                        exprs.extend([
                            pl.col(col_name).min().alias(f"{col_name}_min"),
                            pl.col(col_name).max().alias(f"{col_name}_max"),
                            pl.col(col_name).mean().alias(f"{col_name}_mean"),
                            pl.col(col_name).std().alias(f"{col_name}_std")
                        ])
                
                # Execute lazy expressions
                try:
                    result = lf.select(exprs).collect().to_dicts()[0]
                except Exception as e:
                    logger.warning(f"Lazy evaluation failed for {filename}: {e}. Falling back to sample.")
                    result = lf.head(100000).select(exprs).collect().to_dicts()[0]

                # Format results
                for col_name, dtype in schema.items():
                    col_stats = {
                        "File": filename,
                        "Column": col_name,
                        "Missing Values": result.get(f"{col_name}_nulls", "Error"),
                        "Unique Values": result.get(f"{col_name}_unique", "Error"),
                        "Duplicate Records": duplicate_records
                    }
                    if dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
                        col_stats.update({
                            "Minimum": result.get(f"{col_name}_min"),
                            "Maximum": result.get(f"{col_name}_max"),
                            "Average": result.get(f"{col_name}_mean"),
                            "Standard Deviation": result.get(f"{col_name}_std")
                        })
                    stats.append(col_stats)
                
                df_stats = pd.DataFrame(stats)
                report_path = REPORTS_DIR / f"{filename}_profiling.csv"
                df_stats.to_csv(report_path, index=False)
                all_stats[filename] = df_stats
                
            except Exception as e:
                logger.error(f"Error profiling {filename}: {e}")
                
        return all_stats
