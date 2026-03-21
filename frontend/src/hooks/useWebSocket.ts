import { useCallback, useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';

type WebSocketMessage = { type: string; data: unknown; timestamp: number; };

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (event) => { try { const data = JSON.parse(event.data) as WebSocketMessage; setLastMessage(data); if (data.type === 'prediction' && typeof data.data === 'object' && data.data && 'prediction' in (data.data as Record<string, unknown>)) { toast.success(`Nova previsão: ${(data.data as {prediction: string}).prediction}`); } } catch (error) { console.error('Error parsing WebSocket message:', error); } };
    ws.onclose = () => { setIsConnected(false); reconnectTimeoutRef.current = setTimeout(connect, 3000); };
    ws.onerror = (error) => console.error('WebSocket error:', error);
  }, [url]);
  const disconnect = useCallback(() => { if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current); if (wsRef.current) { wsRef.current.close(); wsRef.current = null; } setIsConnected(false); }, []);
  const sendMessage = useCallback((data: unknown) => { if (wsRef.current?.readyState === WebSocket.OPEN) wsRef.current.send(JSON.stringify(data)); }, []);
  useEffect(() => { connect(); return disconnect; }, [connect, disconnect]);
  return { isConnected, lastMessage, sendMessage, disconnect, reconnect: connect };
}
