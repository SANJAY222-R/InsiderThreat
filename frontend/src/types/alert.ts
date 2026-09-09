export type AlertSeverity = "low" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "investigating" | "resolved" | "false_positive";

export interface Alert {
  id: number;
  prediction_id?: number | null;
  employee_id: string;
  severity: AlertSeverity | string;
  status: AlertStatus | string;
  assigned_to?: string | null;
  title: string;
  description?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at?: string;
  resolved_at?: string | null;
}

export interface AlertCreate {
  employee_id: string;
  title: string;
  severity?: string;
  prediction_id?: number;
  description?: string;
  notes?: string;
}

export interface AlertUpdate {
  status?: string;
  severity?: string;
  assigned_to?: string;
  notes?: string;
}
