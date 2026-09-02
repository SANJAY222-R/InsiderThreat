/**
 * useWebSocket Hook
 *
 * WebSocket connection hook for real-time updates.
 *
 * Phase 0: Stub only.
 *
 * TODO (Phase 8): Implement WebSocket connection with auto-reconnect.
 */

export function useWebSocket(_url: string) {
  return {
    isConnected: false,
    lastMessage: null,
    sendMessage: (_message: string) => {},
    connect: () => {},
    disconnect: () => {},
  };
}
