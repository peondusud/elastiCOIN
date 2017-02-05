#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

apt-get update
apt-get install -y git curl ntpdate
apt-get install -y build-essential libxml2-dev libxslt1-dev libffi-dev libssl-dev zlib1g-dev python3-dev python3-lxml python3-pip 
pip3 install -U setuptools
pip3 install Scrapy scrapyd scrapyd-client
#npm install -g scrapoxy

echo "Europe/Paris" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8' /etc/locale.gen
locale-gen
ntpdate 0.fr.pool.ntp.org


# Install JDK8 on debian
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" > /etc/apt/sources.list.d/webupd8team-java.list
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
apt-get update
apt-get install -y oracle-java8-installer

cd /tmp
ES_VERSION=5.2.0

wget -c https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.deb
dpkg -i elasticsearch-${ES_VERSION}.deb 
#not yet 5.2.0 version
pip3 install -U elasticsearch==5.1.0
#pip3 install -U elasticsearch==${ES_VERSION}
systemctl start elasticsearch
#push template
python3 ${BASEDIR}/elasticsearch/setup.py



wget -c https://artifacts.elastic.co/downloads/kibana/kibana-${ES_VERSION}-amd64.deb
dpkg -i kibana-${ES_VERSION}-amd64.deb
#listen from everywhere
sed -i 's|^#\?\(server.host:\).*|\1 "0.0.0.0"|g' /etc/kibana/kibana.yml

systemctl start kibana
