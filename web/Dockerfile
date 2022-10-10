FROM nginx:1.23.1
COPY ./web/nginx.conf /etc/nginx/nginx.conf
COPY ./web/gunicorn.conf /etc/nginx/conf.d/default.conf
COPY ./web/options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ./web/ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem
