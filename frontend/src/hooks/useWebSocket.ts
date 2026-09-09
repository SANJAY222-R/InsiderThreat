import { useState, useEffect, useRef, useCallback } from "react";

interface UseWebSocketOptions {
  autoReconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onMessage?: (data: unknown) => void;
  onError?: (event: Event) => void;
  onOpen?: () => void;
  onClose?: () => void;
}

interface UseWebSocketResult {
  isConnected: boolean;
  lastMessage: unknown | null;
  sendMessage: (message: string | object) => void;
  connect: () => void;
  disconnect: () => void;
}

export function useWebSocket(
  url?: string,
  options: UseWebSocketOptions = {}
): UseWebSocketResult {
  const {
    autoReconnect = true,
    reconnectInterval = 3000,
    maxReconnectAttempts = 5,
    onMessage,
    onError,
    onOpen,
    onClose,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<unknown | null>(null);

  const socketRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimeout = useRef<number | null>(null);

  const defaultUrl = (() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.hostname;
    const port = "8000";
    return `${protocol}//${host}:${port}/ws`;
  })();

  const wsUrl = url || defaultUrl;

  const disconnect = useCallback(() => {
    if (reconnectTimeout.current) {
      window.clearTimeout(reconnectTimeout.current);
      reconnectTimeout.current = null;
    }
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    setIsConnected(false);
  }, []);

  const connect = useCallback(() => {
    disconnect();

    try {
      const ws = new WebSocket(wsUrl);
      socketRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        reconnectAttempts.current = 0;
        onOpen?.();
      };

      ws.onmessage = (event) => {
        let parsedData = event.data;
        try {
          parsedData = JSON.parse(event.data);
        } catch {
          // Plain text message
        }
        setLastMessage(parsedData);
        onMessage?.(parsedData);
      };

      ws.onerror = (event) => {
        onError?.(event);
      };

      ws.onclose = () => {
        setIsConnected(false);
        onClose?.();

        if (autoReconnect && reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current += 1;
          reconnectTimeout.current = window.setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };
    } catch {
      setIsConnected(false);
    }
  }, [wsUrl, autoReconnect, reconnectInterval, maxReconnectAttempts, onMessage, onError, onOpen, onClose, disconnect]);

  const sendMessage = useCallback((message: string | object) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const payload = typeof message === "string" ? message : JSON.stringify(message);
      socketRef.current.send(payload);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    connect,
    disconnect,
  };
}
