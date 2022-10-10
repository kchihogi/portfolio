FROM nginx:1.23.1
COPY ./web/nginx.conf /etc/nginx/nginx.conf
COPY ./web/gunicorn.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/letsencrypt
RUN curl -o /etc/letsencrypt/options-ssl-nginx.conf -LO https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
RUN curl -o /etc/letsencrypt/ssl-dhparams.pem -LO https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem
