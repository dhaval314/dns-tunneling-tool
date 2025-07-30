from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A
import subprocess
import optparse
from encoder import encode_data
import socket
import math

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--message", dest = "message")
    parser.add_option("-s", "--session", dest = "session_id")
    parser.add_option("-i", "--ip", dest = "ip", help="IP address of the DNS server")
    parser.add_option("-p", "--port", dest = "port")
    (options, arguements) = parser.parse_args()

    return options

def create_request(domain):
    d = DNSRecord.question(domain)
    return d


options = get_arguments()
encoded_data = encode_data(options.message)

session_id = options.session_id



dns_server_ip = options.ip
dns_server_port = int(options.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", int(options.port)))

n = len(encoded_data)
chunk_size = 63
total_chunks = math.ceil((n/63))
chunk = 0
for i in range(0, n, chunk_size):
    chunk_data = encoded_data[i:i+chunk_size]
    chunk_id = str(chunk).zfill(2)
    domain = f"{chunk_id}.{total_chunks}.{chunk_data}.{session_id}.tunnel.local"
    query = create_request(domain)
    sock.sendto(query.pack(), (dns_server_ip, dns_server_port))
    print(f"Sent {chunk_id} {chunk_data}")
    chunk += 1

while 1:
    data, addr = sock.recvfrom(514)
    recieved_response = DNSRecord.parse(data)
    if recieved_response:
        print("DNS server recieved the message successfully")
        break

# TODO / Improvements

# [+] Handle chunk reordering with sorting
# [ ] Add support for multiple simultaneous sessions
# [ ] Send responses back to the client (bi-directional)
# [ ] Encrypt the data before encoding
# [ ] Add file transfer support







