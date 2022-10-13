FROM alpine:latest

WORKDIR /app

RUN apk update && \
  apk add openssl

CMD openssl req -x509 -nodes -newkey rsa:4096 -sha256 -days 365 \
  -keyout '${DOMAIN}/privkey.pem' \
  -out '${DOMAIN}/fullchain.pem' \
  -subj "/CN=localhost"
