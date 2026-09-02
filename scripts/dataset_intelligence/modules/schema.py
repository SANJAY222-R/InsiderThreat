import pandas as pd
import polars as pl
from config import METADATA_DIR, logger

class SchemaDiscovery:
    def run(self, inventory_df):
        logger.info("Module 2: Schema Discovery")
        schema_records = []
        
        for _, row in inventory_df.iterrows():
            filepath = row["Absolute Path"]
            filename = row["Filename"]
            logger.info(f"Discovering schema for {filename}...")
            
            try:
                # Use polars to get schema fast
                lf = pl.scan_csv(filepath)
                schema = lf.collect_schema()
                
                # Fetch a sample to check uniqueness and nullability
                sample = lf.head(10000).collect().to_pandas()
                
                order = 1
                for col_name, dtype in schema.items():
                    col_data = sample[col_name]
                    is_nullable = col_data.isnull().any()
                    # A column is likely unique if all non-null sampled values are unique
                    is_unique = (col_data.nunique() == len(col_data.dropna())) and len(col_data.dropna()) > 100
                    
                    is_timestamp = "date" in col_name.lower() or "time" in col_name.lower()
                    is_categorical = col_data.nunique() < 50 and col_data.dtype == "object"
                    is_numerical = pd.api.types.is_numeric_dtype(col_data)
                    
                    schema_records.append({
                        "File": filename,
                        "Column Order": order,
                        "Column Name": col_name,
                        "Data Type": str(dtype),
                        "Nullable": is_nullable,
                        "Unique Candidate": is_unique,
                        "Primary ID Candidate": is_unique and ("id" in col_name.lower()),
                        "Timestamp Column": is_timestamp,
                        "Categorical Column": is_categorical,
                        "Numerical Column": is_numerical
                    })
                    order += 1
            except Exception as e:
                logger.error(f"Error extracting schema for {filename}: {e}")
        
        schema_df = pd.DataFrame(schema_records)
        schema_df.to_csv(METADATA_DIR / "schema_report.csv", index=False)
        
        # Save as Markdown
        with open(METADATA_DIR / "schema_report.md", "w") as f:
            f.write("# Dataset Schema Report\n\n")
            for file, group in schema_df.groupby("File"):
                f.write(f"## {file}\n")
                f.write(group.drop("File", axis=1).to_markdown(index=False))
                f.write("\n\n")
        
        return schema_df
