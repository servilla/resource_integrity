#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: fabfile

:Synopsis:
    Fabric script to interact with remote host(s) - see below for an example
    $ fab data_query -I -i /home/<user>/.ssh/id_rsa -H kimberlite.lternet.edu

:Author:
    servilla
  
:Created:
    10/6/16
"""
from __future__ import print_function


import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('fabfile')


from fabric.api import *


def query_data_entities():
    print(env.user)
    sql = 'psql -U pasta -d pasta -h localhost -c "copy (select ' \
          'resource_id,resource_location,package_id,' \
          'entity_id,sha1_checksum,resource_size from ' \
          'datapackagemanager.resource_registry where ' \
          'resource_type=\'data\') to stdout with csv" > ' \
          '/tmp/data_entities.csv'
    run(sql)
    get('/tmp/data_entities.csv')


def size_compare():
    #TODO: compare computed data size to resource registry data size
    # 1. read data entities to create list of entities
    # 2. iterate over list of entities to perform size check
    # 3. create report
    pass

def hash_compare():
    #TODO: compare computed data hash to resource registry data hash
    # 1. read data entities to create list of entities
    # 2. iterate over list of entities to perform hash check
    # 3. create report
    pass


def main():
    return 0


if __name__ == "__main__":
    main()