FROM alpine:3.6

ENV MY_DEV_LIBS="python3-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev \
                jpeg-dev zlib-dev libjpeg-turbo-dev tiff-dev freetype-dev lcms2-dev libwebp-dev tcl-dev tk-dev openjpeg-dev libpng-dev"

ENV MY_NEEDED_PKGS="python3 python3-tkinter wget ca-certificates libxslt libssl1.0"

RUN apk add --no-cache ${MY_NEEDED_PKGS} ${MY_DEV_LIBS} && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip  && \
    pip3 install -U pip setuptools certifi && \
    pip3 install scrapy scrapyd scrapyd-client dateparser scrapy-mongodb && \
    pip3 install redis pymongo elastalert elasticsearch==5.4.0 && \
    pip3 install Pillow && \
    apk del ${MY_DEV_LIBS} && rm -r /root/.cache

RUN mkdir -p /etc/scrapyd/ /var/lib/scrapyd
COPY scrapyd.conf /etc/scrapyd/scrapyd.conf
VOLUME /var/lib/scrapyd
RUN mkdir -p /var/lib/scrapyd/{eggs,dbs,logs,items}

WORKDIR /var/lib/scrapyd
EXPOSE 6800

CMD ["scrapyd", "--nodaemon", "--pidfile="]
