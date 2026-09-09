import { api } from "./api";
import type { Prediction } from "../types/prediction";

export interface DashboardSummary {
  total_predictions: number;
  total_alerts: number;
  alerts_by_status: Record<string, number>;
  alerts_by_severity: Record<string, number>;
  recent_predictions: Prediction[];
}

export interface ReportRequestPayload {
  report_type: string;
  date_from: string;
  date_to: string;
  format?: string;
}

export interface ReportResponsePayload {
  report_id: number;
  report_type: string;
  status: string;
  download_url?: string | null;
  generated_at?: string | null;
}

export const reportService = {
  async getSummary(): Promise<DashboardSummary> {
    return api.get<DashboardSummary>("/reports/summary");
  },

  async generate(data: ReportRequestPayload): Promise<ReportResponsePayload> {
    return api.post<ReportResponsePayload>("/reports/generate", data);
  },
};
