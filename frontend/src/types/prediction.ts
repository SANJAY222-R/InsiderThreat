export interface Prediction {
  id: number;
  employee_id: string;
  risk_score: number;
  threat_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | string;
  confidence?: number | null;
  explanation: Record<string, unknown>;
  model_version: string;
  created_at: string;
}

export interface PredictionRequest {
  employee_id: string;
  time_window_start?: string;
  time_window_end?: string;
}

export interface BatchPredictionRequest {
  employee_ids: string[];
}
