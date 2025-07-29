from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A
import subprocess
import optparse
from encoder import encode_data
import socket

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--message", dest ="message")
    parser.add_option("-s", "--session", dest="session_id")
    (options, arguements) = parser.parse_args()

    return options

def create_request(domain):
    d = DNSRecord.question(domain)
    return d


options = get_arguments()
encoded_data = encode_data(options.message)
encoded_data += "eom"
session_id = options.session_id



dns_server_ip = "127.0.0.1"
dns_server_port = 53

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

n = len(encoded_data)
chunk_size = 63
chunk = 0
for i in range(0, n, chunk_size):
    chunk_data = encoded_data[i:i+chunk_size]
    chunk_id = str(chunk).zfill(2)
    domain = f"{chunk_id}.{chunk_data}.{session_id}.tunnel.local"
    query = create_request(domain)
    sock.sendto(query.pack(), (dns_server_ip, dns_server_port))
    print(f"Sent {chunk_id} {chunk_data}")
    chunk += 1









