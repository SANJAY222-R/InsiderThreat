/**
 * Dashboard Slice
 *
 * Redux state for dashboard data (threat overview, stats).
 *
 * Phase 0: Stub only.
 */

export interface DashboardState {
  totalAlerts: number;
  activeThreats: number;
  riskDistribution: Record<string, number>;
  isLoading: boolean;
}

export const initialDashboardState: DashboardState = {
  totalAlerts: 0,
  activeThreats: 0,
  riskDistribution: {},
  isLoading: false,
};

// TODO: Implement with createSlice
