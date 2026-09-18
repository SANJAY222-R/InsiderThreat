import { api } from "./api";
import type { Prediction } from "../types/prediction";

export interface ReportsDashboardSummary {
  total_predictions: number;
  total_alerts: number;
  total_reports: number;
  alerts_by_status: Record<string, number>;
  alerts_by_severity: Record<string, number>;
  reports_by_type: Record<string, number>;
  reports_by_format: Record<string, number>;
  last_generated_at?: string | null;
  recent_predictions: Prediction[];
}

export type DashboardSummary = ReportsDashboardSummary;

export interface ReportRequestPayload {
  report_type: string;
  date_from: string;
  date_to: string;
  format?: string;
  title?: string;
}

export interface ReportItem {
  id: number;
  report_id: number;
  title: string;
  report_type: string;
  format: string;
  status: string;
  date_from: string;
  date_to: string;
  summary_metrics?: {
    total_predictions?: number;
    total_alerts?: number;
    avg_risk_score?: number;
    max_risk_score?: number;
    critical_threats?: number;
    high_threats?: number;
    open_alerts?: number;
    resolved_alerts?: number;
    threat_levels?: Record<string, number>;
    alert_severities?: Record<string, number>;
    alert_statuses?: Record<string, number>;
    [key: string]: any;
  };
  download_url?: string | null;
  file_size?: number | null;
  created_by?: string | null;
  created_at?: string | null;
}

export interface TopEntityReportRecord {
  employee_id: string;
  max_risk_score: number;
  threat_level: string;
  confidence: number;
  alert_count: number;
  top_indicators: string;
}

export interface AlertReportRecord {
  id: number;
  employee_id: string;
  severity: string;
  status: string;
  title: string;
  created_at: string | null;
}

export interface PredictionReportRecord {
  id: number;
  employee_id: string;
  risk_score: number;
  threat_level: string;
  confidence: number;
  created_at: string | null;
}

export interface AuditLogReportRecord {
  id: number;
  user_id: string;
  action: string;
  resource_type: string;
  ip_address: string;
  timestamp: string | null;
}

export interface ReportDetailData {
  report_type: string;
  title: string;
  generated_at: string;
  date_from: string;
  date_to: string;
  created_by: string;
  summary: Record<string, any>;
  top_entities: TopEntityReportRecord[];
  recent_alerts: AlertReportRecord[];
  predictions_sample: PredictionReportRecord[];
  audit_logs_sample: AuditLogReportRecord[];
}

export interface ReportDetailItem extends ReportItem {
  data?: ReportDetailData;
}

export const reportService = {
  async getSummary(): Promise<ReportsDashboardSummary> {
    return api.get<ReportsDashboardSummary>("/reports/summary");
  },

  async getReports(params?: {
    report_type?: string;
    format?: string;
    skip?: number;
    limit?: number;
  }): Promise<ReportItem[]> {
    return api.get<ReportItem[]>("/reports/", { params });
  },

  async getReport(id: number): Promise<ReportDetailItem> {
    return api.get<ReportDetailItem>(`/reports/${id}`);
  },

  async generate(data: ReportRequestPayload): Promise<ReportItem> {
    return api.post<ReportItem>("/reports/generate", data);
  },

  async downloadReport(id: number, formatOverride?: string, filename?: string): Promise<void> {
    const params = formatOverride ? { format: formatOverride } : undefined;
    const defaultFilename = filename || `report_${id}.${formatOverride || "pdf"}`;
    return api.downloadBlob(`/reports/${id}/download`, defaultFilename, { params });
  },

  async instantDownload(data: ReportRequestPayload, filename?: string): Promise<void> {
    const defaultFilename = filename || `instant_report_${data.report_type}.${data.format || "pdf"}`;
    return api.downloadBlobPost("/reports/instant-download", data, defaultFilename);
  },

  async deleteReport(id: number): Promise<{ success: boolean; message: string }> {
    return api.delete<{ success: boolean; message: string }>(`/reports/${id}`);
  },
};
