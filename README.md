# elastiCOIN


## Requirements
* python 3.5
  https://docs.python.org/3.5/

* elasticsearch 5.5.1
  https://www.elastic.co/guide/en/elastic-stack/5.5/index.html

* kibana 5.5.1
  https://www.elastic.co/guide/en/kibana/5.5/index.html

* elasticsearch-py==2.3.0
  http://elasticsearch-py.readthedocs.io/en/5.4.0/

* scrapy==1.4.0
  http://doc.scrapy.org/en/1.4/intro/install.html

* scrapyd==1.2.0
  http://scrapyd.readthedocs.io/en/1.2/

* scrapoxy
  http://docs.scrapoxy.io/en/master/

## Install
```
   apt-get update 
   apt-get install build-essential libxml2-dev libxslt-dev python3-dev python3-pip zlib1g-dev libffi-dev libssl-dev openjdk-8-jdk-headless

   wget -c https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.deb
   wget -c https://artifacts.elastic.co/downloads/kibana/kibana-5.5.1-amd64.deb
   dpkg -i elasticsearch-5.5.1.deb kibana-5.5.1-amd64.deb
   pip3 install -U scrapy scrapyd scrapyd-client elasticsearch==5.4.0
``` 


## Run
``` 
   cd scrapy/
   scrapy crawl lbc
```
Or 
``` 
   scrapy crawl lbc -a url=XXX
``` 
Where XXX is the starting url to crawl

## Run with scrapyd
Launch scrapyd
```
nohup scrapyd
```

First cd into scrapy project's root
```
cd scrapy/
```
Deploy lbc scrapy project
```
crapyd-deploy leboncoin -p leboncoin
```

Launch lbc scrapper
```
curl -XPOST http://localhost:6800/schedule.json -d project=leboncoin -d spider=lbc  -d url=XXX
```

Hint: List available spiders
```
scrapy list
```
