/**
 * Alert Type Definitions
 */

export type AlertSeverity = "info" | "warning" | "critical";
export type AlertStatus = "open" | "investigating" | "resolved" | "false_positive";

export interface Alert {
  id: number;
  predictionId: number;
  severity: AlertSeverity;
  status: AlertStatus;
  assignedTo: number | null;
  notes: string;
  createdAt: string;
  resolvedAt: string | null;
}
