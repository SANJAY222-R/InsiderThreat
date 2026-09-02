/**
 * Application Constants
 *
 * Shared constants for the frontend.
 */

export const APP_NAME = "Insider Threat Detection System";
export const APP_VERSION = "0.1.0";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const THREAT_LEVELS = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
} as const;

export const ALERT_STATUSES = {
  OPEN: "open",
  INVESTIGATING: "investigating",
  RESOLVED: "resolved",
  FALSE_POSITIVE: "false_positive",
} as const;

export const NODE_TYPE_COLORS: Record<string, string> = {
  user: "#4F46E5",
  device: "#10B981",
  email: "#F59E0B",
  file: "#EF4444",
  url: "#8B5CF6",
  pc: "#6B7280",
};
