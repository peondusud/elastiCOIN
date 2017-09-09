#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import argparse

#pip3 install elasticsearch
from elasticsearch import Elasticsearch, helpers 
from datetime import date, datetime
from json import loads, dumps
from itertools import islice


tmplt = """
{
	"mappings": {
		"lbc": {
			"properties": {
				"activites": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256

				},
				"ad_type": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"ad_url": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"age": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"annee": {
					"include_in_all": false,
					"type": "integer"
				},
				"anneemax": {
					"include_in_all": false,
					"type": "integer"
				},
				"anneemin": {
					"include_in_all": false,
					"type": "integer"
				},
				"booster": {
					"include_in_all": false,
					"type": "integer"
				},
				"boutique_id": {
					"include_in_all": false,
					"type": "integer"
				},
				"boutique_name": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"capacite": {
					"include_in_all": false,
					"type": "integer"
				},
				"capacitemax": {
					"include_in_all": false,
					"type": "integer"
				},
				"capacitemin": {
					"include_in_all": false,
					"type": "integer"
				},
				"cat": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"cat_id": {
					"include_in_all": false,
					"type": "integer"
				},
				"cc": {
					"include_in_all": false,
					"type": "integer"
				},
				"ccmax": {
					"include_in_all": false,
					"type": "integer"
				},
				"ccmin": {
					"include_in_all": false,
					"type": "integer"
				},
				"chambre": {
					"include_in_all": false,
					"type": "integer"
				},
				"chambremax": {
					"include_in_all": false,
					"type": "integer"
				},
				"chambremin": {
					"include_in_all": false,
					"type": "integer"
				},
				"check_date": {
					"format": "yyyy.MM.dd HH:mm:ss",
					"include_in_all": false,
					"type": "date"
				},
				"check_epoch": {
					"include_in_all": false,
					"type": "integer"
				},
				"city": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"compte": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"cp": {
					"include_in_all": false,
					"type": "integer"
				},
				"daily_bump": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"daily_bump30": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"datemax": {
					"include_in_all": false,
					"type": "integer"
				},
				"datemin": {
					"include_in_all": false,
					"type": "integer"
				},
				"departement": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"description": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"etudes": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"experience": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"fonction": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"gallery": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"gallery30": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"ges": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"km": {
					"include_in_all": false,
					"type": "integer"
				},
				"kmmax": {
					"include_in_all": false,
					"type": "integer"
				},
				"kmmin": {
					"include_in_all": false,
					"type": "integer"
				},
				"last_update_date": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"ldv": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"listid": {
					"include_in_all": false,
					"type": "long"
				},
				"location": {
					"include_in_all": false,
					"type": "geo_point"
				},
				"loyer": {
					"include_in_all": false,
					"type": "integer"
				},
				"loyermax": {
					"include_in_all": false,
					"type": "integer"
				},
				"loyermin": {
					"include_in_all": false,
					"type": "integer"
				},
				"marque": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"meuble": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"modele": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"nbphoto": {
					"include_in_all": false,
					"type": "integer"
				},
				"nrj": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"oas_cat": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"oas_departement": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"oas_region": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"oas_subcat": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"offres": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"pagename": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"pagetype": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"photosup": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"pieces": {
					"include_in_all": false,
					"type": "integer"
				},
				"piecesmax": {
					"include_in_all": false,
					"type": "integer"
				},
				"piecesmin": {
					"include_in_all": false,
					"type": "integer"
				},
				"piscine": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"prix": {
					"include_in_all": false,
					"type": "integer"
				},
				"prixmax": {
					"include_in_all": false,
					"type": "integer"
				},
				"prixmin": {
					"include_in_all": false,
					"type": "integer"
				},
				"publish_date": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"race": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"region": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"siren": {
					"include_in_all": false,
					"type": "integer"
				},
				"store_id_annonceur": {
					"include_in_all": false,
					"type": "integer"
				},
				"sub_toplist": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"subcat": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"subcat_id": {
					"include_in_all": false,
					"type": "integer"
				},
				"surface": {
					"include_in_all": false,
					"type": "integer"
				},
				"surfacemax": {
					"include_in_all": false,
					"type": "integer"
				},
				"surfacemin": {
					"include_in_all": false,
					"type": "integer"
				},
				"taille": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"temps": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"title": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"titre": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"type": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				},
				"upload_date": {
					"format": "yyyy.MM.dd HH:mm:ss",
					"include_in_all": false,
					"type": "date"
				},
				"upload_epoch": {
					"include_in_all": false,
					"type": "integer"
				},
				"uploader_id": {
					"include_in_all": false,
					"type": "integer"
				},
				"urgent": {
					"include_in_all": false,
					"type": "integer"
				},
				"vitesse": {
					"include_in_all": false,
					"type": "keyword",
					"ignore_above": 256
				}
			}
		}
	},
	"settings": {
		"number_of_replicas": 0,
		"number_of_shards": 2,
		"refresh_interval": "30s"
	},
	"template": "lbc-*"
}
"""



if __name__ == '__main__':
	fmt = '%(asctime)-15s [%(levelname)s] [%(module)s] %(message)s'
	logging.basicConfig(format=fmt)
	logger = logging.getLogger(__name__)
	logger.setLevel( 'INFO' )

	tracer = logging.getLogger('elasticsearch.trace')
	tracer.setLevel('DEBUG')
	#tracer.addHandler(logging.StreamHandler())
	tracer.addHandler(logging.NullHandler())
	#tracer.propagate = False

	parser = argparse.ArgumentParser( description='lbc ES template ' )
	parser.add_argument('-H', '--host', default='127.0.0.1', help='ES host' )
	parser.add_argument('-P', '--port', default=9200, type=int, help='ES port' )
	args = parser.parse_args()

	logger.info(os.environ.get('ES_HOST'))
	host = os.environ.get('ES_HOST', args.host)
	port = os.environ.get('ES_PORT', args.port)
	logger.info("host=> {} port=> {}".format(host, port))
	while True:
		time.sleep(2)
		try:
			es = Elasticsearch([{'host': host, 'port': port}])
			logger.info(es.info())
			logger.info("Try to put lbc template")
			ret = es.indices.put_template(name='lbc', body=tmplt, create=False )
			logger.info(ret)
			sys.exit(0)
		except OSError:
			logger.info("Can't connect to ES cluster")
