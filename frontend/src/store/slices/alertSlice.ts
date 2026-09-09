import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { Alert } from "../../types/alert";

export interface AlertSliceState {
  alerts: Alert[];
  selectedAlert: Alert | null;
  filters: {
    status?: string;
    severity?: string;
    search?: string;
  };
  isLoading: boolean;
  error: string | null;
}

const initialState: AlertSliceState = {
  alerts: [],
  selectedAlert: null,
  filters: {},
  isLoading: false,
  error: null,
};

export const alertSlice = createSlice({
  name: "alerts",
  initialState,
  reducers: {
    setAlerts(state, action: PayloadAction<Alert[]>) {
      state.alerts = action.payload;
      state.isLoading = false;
      state.error = null;
    },
    addAlert(state, action: PayloadAction<Alert>) {
      state.alerts.unshift(action.payload);
    },
    updateAlertInStore(state, action: PayloadAction<Alert>) {
      const idx = state.alerts.findIndex((a) => a.id === action.payload.id);
      if (idx !== -1) {
        state.alerts[idx] = action.payload;
      }
      if (state.selectedAlert?.id === action.payload.id) {
        state.selectedAlert = action.payload;
      }
    },
    setSelectedAlert(state, action: PayloadAction<Alert | null>) {
      state.selectedAlert = action.payload;
    },
    setFilters(state, action: PayloadAction<{ status?: string; severity?: string; search?: string }>) {
      state.filters = action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.isLoading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

export const {
  setAlerts,
  addAlert,
  updateAlertInStore,
  setSelectedAlert,
  setFilters,
  setLoading,
  setError,
} = alertSlice.actions;

export default alertSlice.reducer;
