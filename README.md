# elastiCOIN

  
## 1. Debian way
```bash
apt-get install git
git clone https://github.com/peondusud/elastiCOIN.git
cd elastiCOIN/
bash install.sh
```

  - ### Scrapy run
```bash
cd scrapy; scrapy crawl lbc -a url=URL_TO_CRAWL
```

  - ### Scrapyd run
```bash
nohup scrapyd
cd scrapy; scrapyd-deploy leboncoin -p leboncoin
curl -XPOST http://127.0.0.1:6800/schedule.json -d project=leboncoin -d spider=lbc -d url=URL_TO_CRAWL
```
> #### Launch lbc spider



## 2. Docker way

  - ### Docker requirements
    * [Docker CE](https://docs.docker.com/engine/installation/) 
    * [Docker Compose](https://docs.docker.com/compose/install/) 

  - ### Docker build 
```bash
cd docker\alpine-py3-scrapyd; docker build  -t alpine-py3-scrapyd .; cd ..;
docker-compose up
```

  - ### Docker Launch spider
```bash
curl -XPOST http://127.0.0.1:6800/schedule.json -d project=leboncoin -d spider=lbc -d setting=ES_HOST=elasticsearch -d url=URL_TO_CRAWL
```
```powershell
$params = @{project='leboncoin';spider='lbc';setting='ES_HOST=elasticsearch';url='URL_TO_CRAWL'}
Invoke-WebRequest -Uri "http://127.0.0.1:6800/schedule.json" -Method POST -Body $params
```

> Finally [Visit Kibana!](http://127.0.0.1:5601/) 
