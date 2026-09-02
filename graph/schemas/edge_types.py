"""
Graph Edge Type Definitions
============================

Defines all edge types (relations) in the heterogeneous enterprise graph.

Edge Types:
    - LOGON: User logs onto PC
    - LOGOFF: User logs off PC
    - DEVICE_CONNECT: User connects removable device
    - DEVICE_DISCONNECT: User disconnects removable device
    - EMAIL_SEND: User sends email
    - EMAIL_RECEIVE: User receives email
    - FILE_COPY: User copies file to removable media
    - HTTP_VISIT: User visits URL
    - WORKS_WITH: User-User organizational relationship
    - ASSIGNED_TO: User assigned to PC

Phase 0: Enum and schema definitions.
"""

from enum import Enum

__all__ = ["EdgeType", "EDGE_SCHEMA"]


class EdgeType(str, Enum):
    """Enumeration of all edge types in the heterogeneous graph."""

    LOGON = "logon"
    LOGOFF = "logoff"
    DEVICE_CONNECT = "device_connect"
    DEVICE_DISCONNECT = "device_disconnect"
    EMAIL_SEND = "email_send"
    EMAIL_RECEIVE = "email_receive"
    FILE_COPY = "file_copy"
    HTTP_VISIT = "http_visit"
    WORKS_WITH = "works_with"
    ASSIGNED_TO = "assigned_to"


# Edge schema: (source_node_type, relation, target_node_type)
EDGE_SCHEMA: dict[EdgeType, tuple[str, str, str]] = {
    EdgeType.LOGON: ("user", "logon", "pc"),
    EdgeType.LOGOFF: ("user", "logoff", "pc"),
    EdgeType.DEVICE_CONNECT: ("user", "device_connect", "device"),
    EdgeType.DEVICE_DISCONNECT: ("user", "device_disconnect", "device"),
    EdgeType.EMAIL_SEND: ("user", "email_send", "email"),
    EdgeType.EMAIL_RECEIVE: ("email", "email_receive", "user"),
    EdgeType.FILE_COPY: ("user", "file_copy", "file"),
    EdgeType.HTTP_VISIT: ("user", "http_visit", "url"),
    EdgeType.WORKS_WITH: ("user", "works_with", "user"),
    EdgeType.ASSIGNED_TO: ("user", "assigned_to", "pc"),
}
