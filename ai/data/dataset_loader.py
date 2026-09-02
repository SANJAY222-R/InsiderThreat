"""
Dataset Loader
==============

Loads CERT r4.2 dataset into PyTorch Geometric HeteroData format.

Dataset files:
    - logon.csv    (id, date, user, pc, activity)
    - device.csv   (id, date, user, pc, activity)
    - http.csv     (id, date, user, pc, url, content)
    - email.csv    (id, date, user, pc, to, cc, bcc, from, size, attachment_count, content)
    - file.csv     (id, date, user, pc, filename, content)
    - psychometric.csv  (employee_name, user_id, O, C, E, A, N)
    - LDAP/*.csv   (monthly employee directory snapshots)

Phase 0: Stub only.

TODO (Phase 3): Implement data loading pipeline.
"""

__all__ = ["InsiderThreatDataset"]


class InsiderThreatDataset:
    """
    PyTorch Geometric dataset for CERT r4.2 insider threat data.

    Loads raw CSV files, constructs heterogeneous temporal graph,
    and provides train/val/test splits.
    """
    pass
