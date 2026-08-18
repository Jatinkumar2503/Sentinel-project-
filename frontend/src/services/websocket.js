export class WebSocketService {
  constructor(onMessageCallback) {
    this.onMessage = onMessageCallback;
    this.socket = null;
    this.reconnectTimer = null;
  }

  connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log('⚡ Connected to Sentinel AI WebSocket Hub');
    };

    this.socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (this.onMessage) {
          this.onMessage(payload);
        }
      } catch (err) {
        console.error('Error parsing WS message:', err);
      }
    };

    this.socket.onclose = () => {
      console.warn('⚠️ WebSocket disconnected. Reconnecting in 3s...');
      this.reconnectTimer = setTimeout(() => this.connect(), 3000);
    };

    this.socket.onerror = (err) => {
      console.error('WebSocket Error:', err);
      this.socket.close();
    };
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.socket) this.socket.close();
  }
}
