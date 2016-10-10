#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: file_size_check
    Perform file system level check against file sizes for data entity resources
    found in PASTA's resource registry.

:Synopsis:

:Author:
    servilla
  
:Created:
    10/7/16
"""
from __future__ import print_function


import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('file_size_check')


import getopt
import sys
from os.path import join, getsize

from list_data_entities import list_data_entities


def main(argv):
    usage = 'Usage: python ./file_size_check -h | [-r report file] ' \
            '<data_entity_file>'
    synopsis = '"file_size_check" will compare data entity sizes with ' \
               'file system file sizes and report any inconsistencies.'

    if len(argv) == 0:
        logger.error(usage)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, 'hr:')
    except getopt.GetoptError as e:
        logger.error('Unrecognized command line flag: {0}'.format(e))
        logger.error(usage)
        sys.exit(1)

    report = sys.stdout

    for opt, arg in opts:
        if opt == '-h':
            print(synopsis)
            print(usage)
            sys.exit(0)
        elif opt == '-r':
            report = open(arg, 'w')
        else:
            logger.error(usage)
            sys.exit(1)

    if len(args) == 0:
        logger.error('No data entity file declared.')
        logger.error(usage)
        sys.exit(1)

    data_entities = args[0]

    entities = list_data_entities(data_entities)
    for entity in entities:
        eparts = entity.split(',')
        epath = eparts[1]
        epid = eparts[2]
        ename = eparts[3]
        efile = join(epath, epid, ename)
        try:
            esize = int(eparts[5])
        except ValueError as e:
            print('ValueError: {0} for {1}'.format(e, entity), file=report)
        try:
            fsize = getsize(efile)
            if not esize == fsize:
                print('{0}: expected {1}, but found {2}'.format(efile, esize,
                                                                fsize),
                      file=report)
        except OSError as e:
            print('OSError: {0}'.format(e), file=report)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])