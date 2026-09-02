/**
 * Alert Slice
 *
 * Redux state for alert management.
 *
 * Phase 0: Stub only.
 */

export interface AlertSliceState {
  alerts: unknown[];
  selectedAlert: null;
  filters: Record<string, string>;
  isLoading: boolean;
}

export const initialAlertState: AlertSliceState = {
  alerts: [],
  selectedAlert: null,
  filters: {},
  isLoading: false,
};

// TODO: Implement with createSlice
