apt-get update
apt-get install -y git curl build-essential libxml2-dev libxslt-dev libffi-dev libssl-dev zlib1g-dev python3-dev python3-lxml python3-pip
pip3 install -U setupytools
pip3 install Scrapy scrapyd scrapyd-client
#npm install -g scrapoxy


# Install JDK8 on debian
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" > /etc/apt/sources.list.d/webupd8team-java.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
apt-get update
apt-get install oracle-java8-installer

cd /tmp
ES_VERSION=5.2.0
wget -c https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.deb
wget -c https://artifacts.elastic.co/downloads/kibana/kibana-${ES_VERSION}-amd64.deb
dpkg -i elasticsearch-${ES_VERSION}.deb kibana-${ES_VERSION}-amd64.deb

#not yet 5.2.0 version
pip3 install -U elasticsearch==5.1.0
#pip3 install -U elasticsearch==${ES_VERSION}
