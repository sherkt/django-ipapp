FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
RUN ./configure \
--with-http_realip_module
