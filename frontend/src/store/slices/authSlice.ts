/**
 * Auth Slice
 *
 * Redux state slice for authentication (user, tokens, loading).
 *
 * Phase 0: Stub only.
 */

export interface AuthState {
  user: null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export const initialAuthState: AuthState = {
  user: null,
  accessToken: null,
  isAuthenticated: false,
  isLoading: false,
};

// TODO: Implement with createSlice
