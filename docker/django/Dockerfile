FROM alpine:latest

RUN apk update && apk add python3 curl

RUN mkdir -p /var/www/html && pip3 install --upgrade pip Django

WORKDIR /var/www/html

COPY config/startup.sh /opt/startup.sh

RUN chmod 755 /opt/startup.sh

CMD /opt/startup.sh
