
#!/usr/bin/env python 

from argparse import ArgumentParser
import binascii
import logging
import socket
import ssl
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(dns, query, ca_path):

    server = (dns, 853)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(80)

    ctx = ssl.create_default_context()
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    ctx.load_verify_locations(ca_path)

    wrapped_socket = ctx.wrap_socket(sock, server_hostname=dns)
    wrapped_socket.connect(server)
    logger.info("Server peer certificate: %s", str(wrapped_socket.getpeercert()))

    tcp_msg = "\x00".encode() + chr(len(query)).encode() + query
    logger.info("Client request: %s", str(tcp_msg))
    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)
    return data


def thread(data, address, socket, dns, ca_path):

    answer = send_message(dns, data, ca_path)
    if answer:
        logger.info("Server reply: %s", str(answer))
        rcode = binascii.hexlify(answer[:6]).decode("utf-8")
        rcode = rcode[11:]
        if int(rcode, 16) == 1:
            logger.error("Error processing the request, RCODE = %s", rcode)
        else:
            logger.info("Proxy OK, RCODE = %s", rcode)
            return_ans = answer[2:]
            socket.sendto(return_ans, address)
    else:
        logger.warn("Empty reply from server.")

if __name__ == "__main__":
   DNS = '1.1.1.1'
   port = 53
   host='0.0.0.0'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.bind((host, port))
      while True:
        data,addr = s.recvfrom(1024)
        thread.start_new_thread(thread,(data, addr, DNS))
   except Exception as e:
      logger.error('Failed to secure: '+ str(e))
      print (e)
      s.close()



