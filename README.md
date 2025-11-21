# Secure Undetectable Backdoor

A stealthy, encrypted backdoor designed for authorized penetration testing and security research. This tool emphasizes encryption, automation, and resiliency to ensure communication secrecy and reliability.

---

## Features

- **TLS Encryption:** All communications are protected via TLS for confidentiality.
- **AES-256 Encryption:** Sensitive data is encrypted with a 256-bit symmetric key for maximum secrecy.
- **Command Isolation:** Commands are executed in isolated processes to reduce detection and improve security.
- **Robust Error Handling:** Automatically recovers from most runtime errors, helping maintain connection stability.
- **Automatic Reconnection:** Regains connection to the controller if the session is interrupted.

---

## Requirements

- Python 3.x
- [`pycryptodome`](https://pypi.org/project/pycryptodome/) library
- TLS-compatible network connection

---

## Installation

Install dependencies:

```sh
pip install pycryptodome
```

---

## Usage

**Backdoor Deployment (Victim Machine):**

```sh
python3 backdoor.py
```

**Start Listener (Attacker Machine):**

```sh
python3 listener.py
```

**Connect Controller (Operator/Handler):**

```sh
python3 controller.py
```

---

## Configuration

For all scripts, configure the following variables as needed:

- `server_ip`: IP address of the listener/attack server
- `server_port`: Port number for the listener
- `key`: Shared AES-256 pre-shared key (must be exactly 32 bytes)

Edit these directly in the script files for secure and correct operation.

---

## Security Considerations

> ⚠️ **Warning:** Use this tool only with explicit permission and for legitimate security research or penetration testing.

- **Key Management:** Safeguard your encryption keys at all times.
- **Network Monitoring:** Ensure your operations are protected from advanced monitoring or intrusion detection systems.
- **Endpoint Protection:** Beware that endpoint security tools may flag suspicious activity.
- **Log Analysis:** Routinely check system and audit logs for traces of unexpected behaviors.

---

## Contributing

Contributions and improvements are welcome! Please submit issues or pull requests via GitHub.

---

## License

This project is licensed under the [MIT License](LICENSE).
