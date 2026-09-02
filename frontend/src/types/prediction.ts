/**
 * Prediction Type Definitions
 */

export interface Prediction {
  predictionId: number;
  employeeId: string;
  riskScore: number;
  threatLevel: "low" | "medium" | "high" | "critical";
  explanation: Record<string, unknown>;
  modelVersion: string;
  timestamp: string;
}

export interface PredictionRequest {
  employeeId: string;
  timeWindowStart?: string;
  timeWindowEnd?: string;
}
