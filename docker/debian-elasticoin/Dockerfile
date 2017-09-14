FROM debian:stretch

MAINTAINER peondusud
LABEL Description="Scrapy with python3 docker image based on debian strech"


ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV MY_LOCALE "fr_FR.UTF-8 UTF-8"
ENV MY_DEV_LIBS="apt-utils build-essential libxml2-dev libxslt-dev python3-dev python3-pip python3-setuptools zlib1g-dev libffi-dev libssl-dev"
ENV NEEDED_BIN="curl git supervisor wget unzip ntpdate python3 locales"


RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils  && \
    #apt-get install -y --no-install-recommends install unattended-upgrades needrestart debian-security-support
    apt-get install -y --no-install-recommends ${NEEDED_BIN} ${MY_DEV_LIBS} && \
    apt-get -y -u dist-upgrade && \
    pip3 install -U pip setuptools wheel && \
    pip3 install scrapy scrapyd scrapyd-client dateparser && \
    pip3 install pymongo elasticsearch==5.4.0 elastalert && \
    apt-get autoremove -y --purge ${MY_DEV_LIBS} && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


#set timezone and locale
RUN sed -i -e "s/# ${MY_LOCALE}/${MY_LOCALE}/" /etc/locale.gen && \
    locale-gen && \
    echo "tzdata tzdata/Areas select Europe" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Europe select Paris" | debconf-set-selections && \
    dpkg-reconfigure -f noninteractive tzdata && \
    ntpdate -s 0.fr.pool.ntp.org ; echo

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf
RUN mkdir -p /etc/scrapyd/ /var/lib/scrapyd/{eggs,dbs,logs,items}


USER root

ENV LOG_D /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p ${LOG_D} && \
  chgrp staff ${LOG_D} && \
  chmod g+w ${LOG_D} && \
  chgrp staff /etc/supervisor/conf.d/supervisord.conf

RUN cd /tmp && git clone https://github.com/peondusud/elastiCOIN.git
COPY deploy.sh /tmp/deploy.sh

#scrapyrt
#EXPOSE 9080

#scrapyd
EXPOSE 6800


VOLUME /var/lib/scrapyd/
VOLUME /var/log/supervisor

#CMD ["scrapyd", "--nodaemon"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
