#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads, dumps
from itertools import islice
from elasticsearch import Elasticsearch, helpers #pip install elasticsearch
from datetime import date, datetime
import logging


tmplt = """
{
    "mappings": {
        "lbc": {
            "properties": {
                "addr_locality": {
                    "include_in_all": false,
                    "index": "not_analyzed",
                    "type": "string"
                },
                "c": {
                    "properties": {
                        "activites": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "ad": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "ad_type": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "age": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "cat": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "compte": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "cp": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "departement": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "environnement": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "etudes": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "experience": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "fonction": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "ges": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "km": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "kmmax": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "kmmin": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "last_update_date": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "meuble": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "modele": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "nbphoto": {
                            "include_in_all": false,
                            "type": "short"
                        },
                        "nrj": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "oas_cat": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "offres": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "pagename": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "pagetype": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "race": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "region": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "siren": {
                            "include_in_all": false,
                            "type": "integer"
                        },
                        "store_id_annonceur": {
                            "include_in_all": false,
                            "type": "long"
                        },
                        "subcat": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "taille": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "temps": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "titre": {
                            "fields": {
                                "term": {
                                    "include_in_all": true,
                                    "index": "analyzed",
                                    "type": "string"
                                }
                            },
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "type": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "vitesse": {
                            "include_in_all": false,
                            "index": "not_analyzed",
                            "type": "string"
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
                    "index": "analyzed",
                    "type": "string"
                },
                "doc_id": {
                    "include_in_all": false,
                    "type": "integer"
                },
                "doc_url": {
                    "include_in_all": false,
                    "index": "not_analyzed",
                    "type": "string"
                },
                "img_urls": {
                    "include_in_all": false,
                    "index": "not_analyzed",
                    "type": "string"
                },
                "location": {
                    "include_in_all": false,
                    "type": "geo_point"
                },
                "thumbs_urls": {
                    "include_in_all": false,
                    "index": "not_analyzed",
                    "type": "string"
                },
                "title": {
                    "include_in_all": true,
                    "index": "analyzed",
                    "type": "string"
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
                    "index": "not_analyzed",
                    "type": "string"
                },
                "user_url": {
                    "include_in_all": false,
                    "index": "not_analyzed",
                    "type": "string"
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
    tracer.setLevel('INFO')
    #tracer.addHandler(logging.StreamHandler())
    tracer.addHandler(logging.NullHandler())
    tracer.propagate = False


    es = Elasticsearch([{'host': '127.0.0.1'}])

    logger.info("Try to put lbc template")
    ret = es.indices.put_template(name='lbc', body=tmplt, create=False )

    logger.info(ret)
