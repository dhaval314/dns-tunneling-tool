# DNS Tunneling Tool

A proof-of-concept DNS tunneling tool written in Python. It allows you to encode and transmit arbitrary data from a client to a server by embedding base32-encoded payloads inside DNS queries.

> **Disclaimer**: This tool is for educational purposes only.

---

## Project Structure

```
dns-tunneling-tool/
├── client.py         # Sends DNS queries with encoded data
├── server.py         # Receives DNS queries and extracts data
├── encoder.py        # Base32 encode/decode utility
└── README.md         # This file
```

---

## How It Works

1. The **client**:

   * Takes a message and a session ID
   * Base32 encodes the message
   * Splits it into 63-character chunks
   * Embeds each chunk in a fake DNS query: `<chunk_id>.<data>.<session>.tunnel.local`
   * Sends each query via UDP to a local DNS server

2. The **server**:

   * Listens for incoming DNS queries on port 53
   * Extracts the encoded chunks from the domain name
   * Reassembles them in order
   * Decodes the message and prints it when complete (indicated by `eom`)

---

## Requirements

* Python 3.6+
* `dnslib` library

Install dependencies:

```bash
pip install dnslib
```

---

## Usage

### 1. Start the server

```bash
sudo python3 server.py
```

(Note: port 53 is privileged, so `sudo` is required)

### 2. Run the client

```bash
python3 client.py -m "Hello from client" -s session1
```

You should see the server print the decoded message after receiving all chunks.

---

## Example Output

### Client:

```
Sent 00 NBSWY3DPEB3W64TMMQ
Sent 01 EOM
```

### Server:

```
hello from client
```

---

## Security Warning

DNS tunneling can be used for malicious purposes (e.g. data exfiltration). Do **not** use this tool on production or public networks. Always test in isolated lab environments.

---


