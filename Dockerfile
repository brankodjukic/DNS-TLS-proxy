FROM python:3.6.5-alpine
RUN apk update && apk upgrade 
WORKDIR /usr/local/bin
COPY ./tls-dns.py .
ENTRYPOINT [ "python", "./tls-dns.py"]
EXPOSE 53/tcp
EXPOSE 53/udp



