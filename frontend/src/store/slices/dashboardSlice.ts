import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface DashboardState {
  liveAlerts: any[];
  activeUsers: number;
  criticalIncidents: number;
}

const initialState: DashboardState = {
  liveAlerts: [],
  activeUsers: 0,
  criticalIncidents: 0,
};

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    addLiveAlert(state, action: PayloadAction<any>) {
      state.liveAlerts.unshift(action.payload);
      if (state.liveAlerts.length > 50) state.liveAlerts.pop();
    },
    updateStats(state, action: PayloadAction<{ users: number; critical: number }>) {
      state.activeUsers = action.payload.users;
      state.criticalIncidents = action.payload.critical;
    },
  },
});

export const { addLiveAlert, updateStats } = dashboardSlice.actions;
export default dashboardSlice.reducer;
