FROM nginx:1.31.3-alpine3.24

COPY index.html /usr/share/nginx/html

COPY style.css /usr/share/nginx/html

COPY app.js /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80