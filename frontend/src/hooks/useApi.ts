/**
 * useApi Hook
 *
 * Generic API request hook with loading, error, and data states.
 *
 * Phase 0: Stub only.
 *
 * TODO (Phase 8): Implement with fetch/axios and error handling.
 */

export function useApi<T>(_url: string) {
  // TODO: Implement API request logic
  return {
    data: null as T | null,
    isLoading: false,
    error: null as string | null,
    refetch: async () => {},
  };
}
