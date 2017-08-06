   #!/usr/bin/env bash
   
   BASEDIR=$(dirname "$0")
   ES_VERSION=5.5.1

   apt-get update
   apt-get install -y git curl ntpdate
   apt-get install build-essential libxml2-dev libxslt-dev python3-dev python3-pip zlib1g-dev libffi-dev libssl-dev openjdk-8-jdk-headless git
   pip3 install -U setuptools scrapy scrapyd scrapyd-client elasticsearch==5.4.0
   #npm install -g scrapoxy

   #set timezone and local
   echo "Europe/Paris" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
   sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen
   locale-gen
   ntpdate 0.fr.pool.ntp.org

   cd /tmp
  
   wget -c https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.deb
   dpkg -i elasticsearch-${ES_VERSION}.deb
   systemctl restart elasticsearch
   #push template
   python3 ${BASEDIR}/elasticsearch/setup.py

   wget -c https://artifacts.elastic.co/downloads/kibana/kibana-${ES_VERSION}-amd64.deb
   dpkg -i kibana-${ES_VERSION}-amd64.deb
   #listen from everywhere
   sed -i 's|^#\?\(server.host:\).*|\1 "0.0.0.0"|g' /etc/kibana/kibana.yml
   systemctl restart kibana
  
   cd ${BASEDIR}/scrapy/
   echo -e "please type: \n scrapy crawl lbc or \n scrapy crawl lbc -a url=XXX"
