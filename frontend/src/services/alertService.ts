import { api } from "./api";
import type { Alert, AlertCreate, AlertUpdate } from "../types/alert";

export const alertService = {
  async getAlerts(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    severity?: string;
  }): Promise<Alert[]> {
    return api.get<Alert[]>("/alerts/", { params });
  },

  async getAlert(id: number): Promise<Alert> {
    return api.get<Alert>(`/alerts/${id}`);
  },

  async createAlert(data: AlertCreate): Promise<Alert> {
    return api.post<Alert>("/alerts/", data);
  },

  async updateAlert(id: number, data: AlertUpdate): Promise<Alert> {
    return api.put<Alert>(`/alerts/${id}`, data);
  },
};
