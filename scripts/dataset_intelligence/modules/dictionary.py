import pandas as pd
from config import DICT_DIR, logger

class DictionaryGenerator:
    def run(self, schema_df, profiling_stats):
        logger.info("Module 3: Data Dictionary")
        dictionary_records = []
        
        for _, row in schema_df.iterrows():
            file = row["File"]
            col = row["Column Name"]
            
            # Extract basic profiling stats if available
            missing = "Unknown"
            unique = "Unknown"
            if file in profiling_stats:
                stats_df = profiling_stats[file]
                col_stat = stats_df[stats_df["Column"] == col]
                if not col_stat.empty:
                    missing = col_stat.iloc[0]["Missing Values"]
                    unique = col_stat.iloc[0]["Unique Values"]

            dictionary_records.append({
                "Source File": file,
                "Field Name": col,
                "Data Type": row["Data Type"],
                "Description": f"Auto-generated description for {col} in {file}",
                "Nullable": row["Nullable"],
                "Missing Values": missing,
                "Unique Values": unique,
                "Is Primary Key Candidate": row["Primary ID Candidate"],
                "Is Categorical": row["Categorical Column"]
            })
            
        dict_df = pd.DataFrame(dictionary_records)
        dict_df.to_csv(DICT_DIR / "data_dictionary.csv", index=False)
        
        # Save as Markdown
        with open(DICT_DIR / "data_dictionary.md", "w") as f:
            f.write("# Data Dictionary\n\n")
            for file, group in dict_df.groupby("Source File"):
                f.write(f"## {file}\n")
                f.write(group.drop("Source File", axis=1).to_markdown(index=False))
                f.write("\n\n")
                
        # Save as HTML
        dict_df.to_html(DICT_DIR / "data_dictionary.html", index=False)
        logger.info("Data dictionary generated in CSV, MD, and HTML formats.")
