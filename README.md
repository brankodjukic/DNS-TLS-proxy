# DNS-TLS-proxy
Proxy is used to send DNS queries encrypted. This solves issue with sending DNS query as a plain text. This project was made
for learning purposes. 
DNS over TLS, or DoT, is a standard for encrypting DNS queries to keep them secure and private.
DoT adds TLS encryption on top of the user datagram protocol (UDP), which is used for DNS queries.
This proxy captures DNS requests from the host and redirect it to serverthat support TLS (Cloudflare) and replies to the client.

# Implementation
When recived a query, dns-tls-proxy the thread is started. Wraps a new TCP socket with SLL and verifies the certificate.
The message is formatted and sent to the server over encrypted connection. When gets reply it checks the answer for errors.
If the query is successful forwards the result to the clinet.
It can be used from the terminal as script or a Docker container.

# Security concerns

# Testing
For testing we can use Wireshark, netcat, dig, curl and so on.
