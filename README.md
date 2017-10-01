# elastiCOIN

## 1. Requirements
* [python 3.5](https://docs.python.org/3.5/)

* [elasticsearch 5.6.0](https://www.elastic.co/guide/en/elastic-stack/5.6/index.html)  

* [kibana 5.6.0](https://www.elastic.co/guide/en/kibana/5.6/index.html) 

* [elasticsearch-py==5.4.0](http://elasticsearch-py.readthedocs.io/en/5.4.0/) 
  
* [scrapy==1.4.0](http://doc.scrapy.org/en/1.4/intro/install.html) 
  
* [scrapyd==1.2.0](http://scrapyd.readthedocs.io/en/1.2/) 
  
* [scrapoxy](http://docs.scrapoxy.io/en/master/) 
  
## 2. Debian
```bash
apt-get install git
git clone https://github.com/peondusud/elastiCOIN.git
cd elastiCOIN/
bash install.sh
```

### Run
```bash
cd scrapy; scrapy crawl lbc
```
Or
```bash
cd scrapy; scrapy crawl lbc -a url=XXX
```
*__XXX__ is the starting __url to crawl__*

*Hint: List available spiders*
```bash
scrapy list
```

### Run with scrapyd
Launch scrapyd (daemon)
```bash
nohup scrapyd
```

Deploy lbc scrapy project
```bash
cd scrapy;
scrapyd-deploy leboncoin -p leboncoin
```

Launch lbc spider
```bash
curl -XPOST http://127.0.0.1:6800/schedule.json -d project=leboncoin -d spider=lbc -d url=XXX
```
_Hint: List available spiders_
```bash
curl http://127.0.0.1:6800/listspiders.json
```


## 3. Docker Install
```bash
cd docker\alpine-py3-scrapyd; docker build  -t alpine-py3-scrapyd .; cd ..;
docker-compose up
```
check scrapyd status
```bash
curl http://127.0.0.1:6800/daemonstatus.json
curl http://127.0.0.1:6800/listprojects.json
```

### Docker Launch spider
```bash
curl -XPOST http://127.0.0.1:6800/schedule.json -d project=leboncoin -d spider=lbc -d setting=ES_HOST=elasticsearch -d url=XXX
```
*__XXX__ is the starting __url to crawl__*

Start playing http://127.0.0.1:5601/
