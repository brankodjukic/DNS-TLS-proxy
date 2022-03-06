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
In addition, DNS continues to be a target for DDoS attacks. When DNS goes down, applications will fail to function properly, affecting subscriber experience. It is now more critical than ever for operators to enable dynamic service delivery infrastructure for managing and securing the impending flood of DNS traffic. That's why 
is important to secure it.
I thnik services like this are more secure. We know who is behind it and what exactly is their purpose.
To integrate such service and test it properly in would definity use tools such as Ansible, Docker, Kubernetes and Jenkins. 
# Testing
For testing we can use Wireshark, netcat, dig, curl and so on.
