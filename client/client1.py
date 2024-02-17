
import socket
import ssl
import subprocess
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import sys

if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1);
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False 
    context.load_verify_locations('MyPKISubCAG1-chain.pem')
    context.load_cert_chain(certfile="51690F08190E8784ADEA200D0C946D43BBE91C6D.pem", keyfile="client.key")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False,server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    cert = secure_sock.getpeercert()
    print(cert)
    

    print("Connection is established")
    value=input("Enter text=")
    try:
    	secure_sock.send(value.encode())
    	data=secure_sock.read(1024)
    	msg=data.decode('utf-8') 
    	print (msg)
    except Exception as e:
    	print("Connection error:", e)
    	print("Connection lost")
    

    secure_sock.close()
    sock.close()

