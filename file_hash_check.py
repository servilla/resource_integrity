#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: file_hash_check

:Synopsis:
    Perform file system level check against file SHA1 hashes for data entity
    resources found in PASTA's resource registry.

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
logger = logging.getLogger('file_hash_check')


import getopt
import sys
from os.path import join, getsize
from hashlib import sha1

from list_data_entities import list_data_entities


def sha1sum(file_name):
    hash = sha1()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
            hash.update(chunk)
    return hash.hexdigest()


def main(argv):
    usage = 'Usage: python ./file_hash_check -h | [-r report file] ' \
            '<data_entity_file>'
    synopsis = '"file_hash_check" will compare data entity SHA1 hash value ' \
               'with one generated from the file system object and report ' \
               'any inconsistencies.'

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
            ehash = int(eparts[4])
        except ValueError as e:
            print('ValueError: {0} for {1}'.format(e, entity), file=report)
        try:
            fhash = sha1sum(efile)
            if not ehash == fhash:
                print('{0}: expected {1}, but found {2}'.format(efile, ehash,
                                                                fhash),
                      file=report)
        except IOError as e:
            print('IOError: {0}'.format(e), file=report)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])