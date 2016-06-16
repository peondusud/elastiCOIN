#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from json import loads, dumps
from itertools import islice
from elasticsearch import Elasticsearch, helpers #pip3 install elasticsearch
from datetime import date, datetime
import logging
import argparse

def index_action(json_str):
    dic = loads(json_str)
    index_date = dic["upload_date"][:10]
    ad_id =  dic['c']['listid']
    #"index_date = datetime.datetime.strptime(dic["upload_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y.%m.%d")
    action = { '_op_type': 'index',
                '_index': "lbc-" + index_date,
                '_type': 'lbc',
                '_id': ad_id,
                '_source': json_str 
        }
    return action


if __name__ == '__main__':
    fmt = '%(asctime)-15s [%(levelname)s] [%(module)s] %(message)s'
    logging.basicConfig(format=fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel( 'INFO' )
    log_levels = {
                'CRITICAL': 50,
                'ERROR': 40,
                'WARNING': 30,
                'INFO': 20,
                'DEBUG': 10,
                'NOTSET': 0
    }
    parser = argparse.ArgumentParser( description='lbc center' )
    parser.add_argument( '-f', default='dump_lbc.json' , help='dump lbc path' )
    parser.add_argument( '-level', default='INFO', choices=log_levels.keys() , help='log level' )
    parser.add_argument( '-bulk', default=500, help='Elasticsearch Bulk size' )
    args = parser.parse_args()
    logger.setLevel( log_levels[args.level] )
    es = Elasticsearch([
                        {'host': '127.0.0.1',
                         'port': 9200 }
                       ])
    ES_BULK_SIZE = args.bulk
    print( args)
    logger.info("Start injection")
    with open(args.f, 'r') as fd:
        while True:
            chunk = list(islice(fd, ES_BULK_SIZE))
            if not chunk:
                break
            bulk_actions_buffer = list(map(index_action, chunk))
            success, _ = helpers.bulk( es,
                                        actions = bulk_actions_buffer,
                                        stats_only = True,
                                        raise_on_error = True,
                                        chunk_size = ES_BULK_SIZE
                                    )
            print(success)
    logger.info("End injection")
