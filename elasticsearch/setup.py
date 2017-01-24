#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

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
                "addr_locality": {
                    "include_in_all": false,
                    "type": "keyword"
                },
                "c": {
                    "properties": {
                        "activites": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "ad": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "ad_type": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "age": {
                            "include_in_all": false,
                            "type": "keyword"
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
                        "boutique_id": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "ca_type": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "cat": {
                            "include_in_all": false,
                            "type": "keyword"
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
                        "city": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "compte": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "cp": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "departement": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "environnement": {
                            "include_in_all": false,                            
                            "type": "keyword"
                        },
                        "etudes": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "experience": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "fonction": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "ges": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "km": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "kmmax": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "kmmin": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "last_update_date": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "listid": {
                            "include_in_all": false,
                            "type": "long"
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
                            "type": "keyword"
                        },
                        "meuble": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "modele": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "nbphoto": {
                            "include_in_all": false,
                            "type": "short"
                        },
                        "nrj": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "oas_cat": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "oas_departement": {
                            "include_in_all": false,
                            "type": "short"
                        },
                        "oas_region": {
                            "include_in_all": false,
                            "type": "short"
                        },
                        "oas_subcat": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "offres": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "pagename": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "pagetype": {
                            "include_in_all": false,
                            "type": "keyword"
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
                            "type": "keyword"
                        },
                        "race": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "region": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "siren": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "store_id_annonceur": {
                            "type": "long"
                        },
                        "subcat": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "subcat_id": {
                            "include_in_all": false,
                            "type": "short"
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
                            "type": "keyword"
                        },
                        "taille": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "temps": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "titre": {
                            "fields": {
                                "term": {
                                    "include_in_all": true,
                                    "type": "text"
                                }
                            },
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "type": {
                            "include_in_all": false,
                            "type": "keyword"
                        },
                        "vitesse": {
                            "include_in_all": false,
                            "type": "keyword"
                        }
                    }
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
                "desc": {
                    "include_in_all": true,
                    "type": "text"
                },
                "doc_id": {
                    "include_in_all": false,
                    "type": "integer"
                },
                "doc_url": {
                    "include_in_all": false,
                    "type": "keyword"
                },
                "img_urls": {
                    "include_in_all": false,
                    "type": "keyword"
                },
                "location": {
                    "include_in_all": false,
                    "type": "geo_point"
                },
                "thumbs_urls": {
                    "include_in_all": false,
                    "type": "keyword"
                },
                "title": {
                    "include_in_all": true,
                    "type": "keyword"
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
                "urg": {
                    "include_in_all": false,
                    "type": "short"
                },
                "user_id": {
                    "include_in_all": false,
                    "type": "integer"
                },
                "user_name": {
                    "include_in_all": false,
                    "type": "keyword"
                },
                "user_url": {
                    "include_in_all": false,
                    "type": "keyword"
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


    es = Elasticsearch([{'host': '127.0.0.1'}])

    logger.info("Try to put lbc template")
    ret = es.indices.put_template(name='lbc', body=tmplt, create=False )

    logger.info(ret)
