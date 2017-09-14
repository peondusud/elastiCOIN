FROM alpine:3.6

ENV MY_DEV_LIBS="python3-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev"

RUN apk add --no-cache python3 libxslt ${MY_DEV_LIBS} && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip  && \
    pip3 install -U pip setuptools certifi && \
    pip3 install scrapy scrapyd-client scrapyrt dateparser && \
    pip3 install pymongo elasticsearch==5.4.0 && \
    apk del ${MY_DEV_LIBS} && rm -r /root/.cache


WORKDIR /home

VOLUME /home/
EXPOSE 6800

CMD ["scrapyd", "--nodaemon"]
