import os
from .base_extractor import BaseEntityModule
import logging

logger = logging.getLogger("EntityExtraction")

class RecommendationsGenerator(BaseEntityModule):
    """Module 12: Phase 5 Recommendations"""
    
    def run(self):
        rec_path = os.path.join(self.cfg.paths.reports_dir, "phase5_recommendations.md")
        
        with open(rec_path, "w") as f:
            f.write("# Phase 5 Recommendations: Temporal Graph Construction\n\n")
            f.write("## 1. Graph Storage\n")
            f.write("- **Recommendation:** Neo4j Community Edition or Neo4j Aura.\n")
            f.write("- **Rationale:** Neo4j's property graph model perfectly aligns with the generated schemas, supporting node features easily.\n\n")
            f.write("## 2. Temporal Windows\n")
            f.write("- **Recommendation:** 24-hour sliding windows with 12-hour overlap.\n")
            f.write("- **Rationale:** Captures day-to-day anomalous drifts effectively without massive graph explosion.\n\n")
            f.write("## 3. Graph Schema Topology\n")
            f.write("- Nodes: User, Host, File, USB, Email, Domain, Website\n")
            f.write("- Edges: LOGS_ON (User->Host), ACCESSES (User->File), SENDS (User->Email), CONNECTS (Host->USB)\n\n")
            
        logger.info("Phase 5 Recommendations Generated.")
