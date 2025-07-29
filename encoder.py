import base64

def encode_data(data):

    encoded = base64.b32encode(data.encode('utf-8'))  
    return encoded.decode('utf-8').rstrip('=')        

def decode_data(encoded):

    padding = '=' * ((8 - len(encoded) % 8) % 8)       
    decoded = base64.b32decode((encoded + padding).encode('utf-8'))  
    return decoded.decode('utf-8')                     
