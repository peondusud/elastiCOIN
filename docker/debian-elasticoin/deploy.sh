
set -x
cd /tmp/elastiCOIN/scrapy
sleep 2
/usr/local/bin/scrapyd-deploy leboncoin -p leboncoin -d
echo $?
exit 0
