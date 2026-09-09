import { api } from "./api";
import type { Prediction, PredictionRequest } from "../types/prediction";

export interface ExplanationResponse {
  prediction_id: number;
  employee_id: string;
  risk_score: number;
  threat_level: string;
  explanation: {
    feature_importance: Record<string, number>;
    top_features: Array<{ name: string; value: number; direction: string }>;
    model_version?: string;
    method?: string;
  };
}

export const predictionService = {
  async predict(request: PredictionRequest): Promise<Prediction> {
    return api.post<Prediction>("/predictions/", request);
  },

  async getPredictions(params?: {
    skip?: number;
    limit?: number;
    employee_id?: string;
  }): Promise<Prediction[]> {
    return api.get<Prediction[]>("/predictions/", { params });
  },

  async getPrediction(id: number): Promise<Prediction> {
    return api.get<Prediction>(`/predictions/${id}`);
  },

  async getExplanation(predictionId: number): Promise<ExplanationResponse> {
    return api.get<ExplanationResponse>(`/explain/${predictionId}`);
  },
};
