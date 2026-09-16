import polars as pl
import pandas as pd
from config import REPORTS_DIR, logger

class EntityDiscovery:
    def run(self, inventory_df: pd.DataFrame) -> None:
        logger.info("Module 5 & 6: Entity and Relationship Discovery")
        
        # We will map standard entity columns based on common CERT dataset names
        entity_maps = {
            "user": set(),
            "pc": set(),
            "file_path": set(),
            "email_address": set(),
            "url": set()
        }
        
        relationships = []

        for _, row in inventory_df.iterrows():
            filepath = row["Absolute Path"]
            filename = row["Filename"]
            
            try:
                lf = pl.scan_csv(filepath)
                # Sample for speed if large
                if row["Number of Records"] > 1_000_000:
                    lf = lf.head(1000000)
                columns = lf.columns
                
                # Extract users
                if "user" in columns:
                    users = lf.select("user").drop_nulls().unique().collect().to_series().to_list()
                    entity_maps["user"].update(users)
                
                # Extract hosts (pc)
                if "pc" in columns:
                    pcs = lf.select("pc").drop_nulls().unique().collect().to_series().to_list()
                    entity_maps["pc"].update(pcs)
                    
                # Relationships User -> Host
                if "user" in columns and "pc" in columns:
                    rel_count = lf.select(["user", "pc"]).unique().select(pl.len()).collect().item()
                    relationships.append({"Source": "User", "Target": "Host", "Context": filename, "Unique Edges": rel_count})
                    
                # Other entities based on specific files
                if filename == "email.csv":
                    if "to" in columns:
                        # naive extraction for speed
                        emails = lf.head(100000).select("to").drop_nulls().unique().collect().to_series().to_list()
                        entity_maps["email_address"].update([e for e in emails if isinstance(e, str)])
                    if "user" in columns and "to" in columns:
                        relationships.append({"Source": "User", "Target": "Email", "Context": filename, "Unique Edges": "Estimated via Emails"})
                
                if filename == "file.csv":
                    if "filename" in columns:
                        files = lf.head(100000).select("filename").drop_nulls().unique().collect().to_series().to_list()
                        entity_maps["file_path"].update(files)
                    if "user" in columns and "filename" in columns:
                        relationships.append({"Source": "User", "Target": "File", "Context": filename, "Unique Edges": "Estimated via Files"})
                        
                if filename == "http.csv":
                    if "url" in columns:
                        urls = lf.head(100000).select("url").drop_nulls().unique().collect().to_series().to_list()
                        entity_maps["url"].update(urls)
                    if "user" in columns and "url" in columns:
                        relationships.append({"Source": "User", "Target": "Website", "Context": filename, "Unique Edges": "Estimated via URLs"})
                        
            except Exception as e:
                logger.error(f"Error during entity extraction in {filename}: {e}")
        
        # Save entities
        for ent_name, ent_set in entity_maps.items():
            if ent_set:
                df = pd.DataFrame({ent_name: list(ent_set)})
                df.to_csv(REPORTS_DIR / f"entities_{ent_name}.csv", index=False)
                
        # Save relationships
        rel_df = pd.DataFrame(relationships)
        rel_df.to_csv(REPORTS_DIR / "relationship_summary.csv", index=False)
        logger.info(f"Entities and relationships saved.")
