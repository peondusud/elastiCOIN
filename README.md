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
    apt-get install git
    git clone https://github.com/peondusud/elastiCOIN.git
    cd elastiCOIN/
    bash install.sh
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
