import socket
from dnslib import DNSRecord
import re
from encoder import decode_data
import time
port = 53
ip = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((ip, port))
message = ""

while 1:
    data, addr = sock.recvfrom(512)
    response = DNSRecord.parse(data)
    pattern = r"\d+\.[A-Za-z\d]+\.[A-Za-z\d]+\.[A-Za-z\d]+\.[A-Za-z\d]+"
    matched = re.search(pattern, str(response))
    if matched:
        encoded_message = matched.group(0).split(".")
        message += encoded_message[1]  
    # print(message[-3:])
    if message[-3:] == "eom":
        decoded_message = decode_data(message[:-3])
        print(decoded_message)
        message = ""
   
    
    
    


