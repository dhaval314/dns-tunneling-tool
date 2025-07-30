import socket
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A
import re
from encoder import decode_data
from collections import defaultdict
port = 53
ip = "127.0.0.2"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((ip, port))
message = defaultdict()
final_encoded_message = ""
chunks = 0
while 1:
    data, addr = sock.recvfrom(512)

    response = DNSRecord.parse(data)
    pattern = r"\d+\.\d+\.[A-Za-z\d]+\.[A-Za-z\d]+\.[A-Za-z\d]+\.[A-Za-z\d]+" # pattern for the dns query
    matched = re.search(pattern, str(response))
    if matched:
        encoded_message = matched.group(0).split(".") 
        message[int(encoded_message[0])] = encoded_message[2]
        chunks += 1
        

    # if we recieve the last chunk
    if int(matched.group(0).split(".")[1]) == chunks:

        arranged_msg = dict(sorted(message.items())) # sorting if the chunks are recieved out of order

        for encoded_chunk in arranged_msg.values():
            final_encoded_message += encoded_chunk
        
        final_decoded_message = decode_data(final_encoded_message)
        print(final_decoded_message)

        # resetting for data that might be sent later
        chunks = 0
        final_encoded_message = ""

        # responding when the message is fully recieved
        response = DNSRecord(DNSHeader(qr=1,aa=1,ra=1),
                  q=DNSQuestion(""),
                  a=RR("",rdata=A("123.12.12.12")))
        
        sock.sendto(response.pack(), (addr[0], addr[1]))
        response = None
        
    
