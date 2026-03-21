export type RealtimeMessage = { type: string; data: unknown; timestamp: number };

export class WebSocketService {
  private socket: WebSocket | null = null;
  connect(url: string, onMessage: (message: RealtimeMessage) => void) {
    this.socket = new WebSocket(url);
    this.socket.onmessage = (event) => onMessage(JSON.parse(event.data) as RealtimeMessage);
    return this.socket;
  }
  send(payload: unknown) {
    if (this.socket?.readyState === WebSocket.OPEN) this.socket.send(JSON.stringify(payload));
  }
  disconnect() {
    this.socket?.close();
    this.socket = null;
  }
}
