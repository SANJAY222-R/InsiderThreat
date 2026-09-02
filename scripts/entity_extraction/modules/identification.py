import polars as pl
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class EntityIdentifier(BaseEntityModule):
    """Module 1: Entity Identification"""
    
    def run(self) -> dict:
        entities = {
            "users": set(),
            "hosts": set(),
            "files": set(),
            "usbs": set(),
            "emails": set(),
            "domains": set(),
            "websites": set(),
            "urls": set(),
            "departments": set(),
            "sessions": set()
        }
        
        # 1. Logon Data
        logon_df = self.load_processed("logon")
        if logon_df is not None:
            if "user" in logon_df.columns: entities["users"].update(logon_df["user"].unique().to_list())
            if "pc" in logon_df.columns: entities["hosts"].update(logon_df["pc"].unique().to_list())
                
        # 2. File Data
        file_df = self.load_processed("file")
        if file_df is not None:
            if "user" in file_df.columns: entities["users"].update(file_df["user"].unique().to_list())
            if "pc" in file_df.columns: entities["hosts"].update(file_df["pc"].unique().to_list())
            if "filename" in file_df.columns: entities["files"].update(file_df["filename"].unique().to_list())
                
        # 3. Device Data (USBs)
        dev_df = self.load_processed("device")
        if dev_df is not None:
            # We don't have explicit USB ID in standard CERT dev, so we use 'pc' or a placeholder if missing
            if "user" in dev_df.columns: entities["users"].update(dev_df["user"].unique().to_list())
            if "pc" in dev_df.columns: entities["hosts"].update(dev_df["pc"].unique().to_list())
            # In some datasets, id is device id. We will use the 'id' column as USB event ID, or 'pc' as proxy for connected device.
            if "id" in dev_df.columns: entities["usbs"].update(dev_df["id"].unique().to_list())
                
        # 4. Email Data
        email_df = self.load_processed("email")
        if email_df is not None:
            if "user" in email_df.columns: entities["users"].update(email_df["user"].unique().to_list())
            if "pc" in email_df.columns: entities["hosts"].update(email_df["pc"].unique().to_list())
            if "to" in email_df.columns: entities["emails"].update(email_df["to"].unique().to_list())
            if "from" in email_df.columns: entities["emails"].update(email_df["from"].unique().to_list())
                
        # 5. HTTP Data
        http_df = self.load_processed("http")
        if http_df is not None:
            if "user" in http_df.columns: entities["users"].update(http_df["user"].unique().to_list())
            if "pc" in http_df.columns: entities["hosts"].update(http_df["pc"].unique().to_list())
            if "url" in http_df.columns: entities["urls"].update(http_df["url"].unique().to_list())
                
        # Remove nulls
        for k in entities.keys():
            entities[k] = {e for e in entities[k] if e is not None and str(e).strip() != ""}
            
        logger.info(f"Identified {len(entities['users'])} Users, {len(entities['hosts'])} Hosts, {len(entities['files'])} Files.")
        
        # Convert sets to DataFrames with 'raw_id'
        df_entities = {}
        for k, v in entities.items():
            if len(v) > 0:
                df_entities[k] = pl.DataFrame({"raw_id": list(v)})
            else:
                df_entities[k] = pl.DataFrame({"raw_id": []}, schema={"raw_id": pl.Utf8})
                
        return df_entities
