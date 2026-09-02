/**
 * useAuth Hook
 *
 * Authentication state management hook.
 * Provides login, logout, and current user state.
 *
 * Phase 0: Stub only.
 *
 * TODO (Phase 8): Implement with JWT token management.
 */

export function useAuth() {
  // TODO: Implement authentication logic
  return {
    user: null,
    isAuthenticated: false,
    isLoading: false,
    login: async (_username: string, _password: string) => {},
    logout: async () => {},
    refreshToken: async () => {},
  };
}
