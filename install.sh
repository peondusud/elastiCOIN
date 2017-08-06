   apt-get update 
   apt-get install build-essential libxml2-dev libxslt-dev python3-dev python3-pip zlib1g-dev libffi-dev libssl-dev openjdk-8-jdk-headless git

   wget -c https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.deb
   wget -c https://artifacts.elastic.co/downloads/kibana/kibana-5.5.1-amd64.deb
   dpkg -i elasticsearch-5.5.1.deb kibana-5.5.1-amd64.deb
   pip3 install -U scrapy scrapyd scrapyd-client elasticsearch==5.4.0

   
   git clone https://github.com/peondusud/elastiCOIN.git
   cd elastiCOIN/
   systemctl restart elasticsearch
   python3 elasticsearch/setup.py

   systemctl restart kibana
   cd scrapy/
   echo -e "please type: \n scrapy crawl lbc or \n scrapy crawl lbc -a url=XXX"
