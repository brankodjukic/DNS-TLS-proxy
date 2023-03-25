#!/usr/bin/env python3

import argparse
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

    tcp_msg = b"\x00" + bytes([len(query)]) + query.encode()
    logger.info("Client request: %s", str(tcp_msg))
    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)
    return data


def thread(data, address, dns, ca_path):
    answer = send_message(dns, data.decode(), ca_path)
    if answer:
        logger.info("Server reply: %s", str(answer))
        rcode = binascii.hexlify(answer[:6]).decode("utf-8")
        rcode = rcode[11:]
        if int(rcode, 16) == 1:
            logger.error("Error processing the request, RCODE = %s", rcode)
        else:
            logger.info("Proxy OK, RCODE = %s", rcode)
            return_ans = answer[2:]
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(return_ans, address)
    else:
        logger.warning("Empty reply from server.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dns", default="1.1.1.1", help="DNS server IP address")
    parser.add_argument("--port", type=int, default=53, help="Port to listen on")
    parser.add_argument("--host", default="0.0.0.0", help="Host IP address to bind to")
    parser.add_argument("--ca_path", default="/etc/ssl/cert.pem", help="Path to the CA file")
    args = parser.parse_args()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((args.host, args.port))
        while True:
            data, addr = s.recvfrom(1024)
            threading.Thread(target=thread, args=(data, addr, args.dns, args.ca_path)).start()
    except Exception as e:
        logger.error('Failed to secure: '+ str(e))
        print (e)
        s.close()
