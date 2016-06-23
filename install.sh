curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
apt-get update
apt-get install build-essential libxml2-dev libxslt-dev python-dev python-lxml nodejs git

cd /tmp
wget -c https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.3/elasticsearch-2.3.3.deb
wget -c https://download.elastic.co/kibana/kibana/kibana_4.5.1_amd64.deb
dpkg -i elasticsearch-2.3.3.deb kibana_4.5.1_amd64.deb
pip install -U scrapy scrapyd scrapyd-client elasticsearch==2.3.0
npm install -g scrapoxy

