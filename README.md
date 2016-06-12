# elastiCOIN


Requirements
============
python 2.7

elasticsearch 2.3.3

https://www.elastic.co/downloads/elasticsearch

kibana 4.5.1

https://www.elastic.co/downloads/kibana

elasticsearch-py==2.3

https://elasticsearch-py.readthedocs.org/en/master/index.html

scrapy==1.1.0

http://doc.scrapy.org/en/latest/intro/install.html



Install
=======
``` 
   apt-get install libxml2-dev libxslt-dev python-dev python-lxml
``` 
```
   wget -c https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.3/elasticsearch-2.3.3.deb 
   wget -c https://download.elastic.co/kibana/kibana/kibana_4.5.1_amd64.deb
   dpkg -i elasticsearch-2.3.3.deb kibana_4.5.1_amd64.deb
   pip install -U scrapy scrapyd elasticsearch==2.3.0
``` 


Run

``` 
   cd scrapy/
   scrapy crawl lbc
``` 
