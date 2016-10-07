#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: list_data_entities

:Synopsis:

:Author:
    servilla
  
:Created:
    10/7/16
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('list_data_entities')


import sys


def list_data_entities(sql_dump_file = None):
    lines = [line.rstrip('\n') for line in open(sql_dump_file)]
    return lines

def main():

    list_data_entities(sys.argv[1])

    return 0


if __name__ == "__main__":
    main()