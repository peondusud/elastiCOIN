FROM alpine:3.6

ENV MY_DEV_LIBS="python3-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev"

RUN apk add --no-cache python3 curl libxslt ${MY_DEV_LIBS} && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip  && \
    pip3 install -U pip setuptools certifi && \
    pip3 install scrapy scrapyd scrapyd-client dateparser && \
    pip3 install pymongo elasticsearch==5.4.0 elastalert && \
    apk del ${MY_DEV_LIBS} && rm -r /root/.cache


RUN curl -L -s https://github.com/just-containers/s6-overlay/releases/download/v1.20.0.0/s6-overlay-amd64.tar.gz \
     | tar xvzf - -C /

WORKDIR /home
COPY scrapyd.conf .

VOLUME /home/
EXPOSE 6800

ENTRYPOINT ["/init"]
