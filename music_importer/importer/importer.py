# -*- coding: utf-8 -*-
'''
Created on Nov 1, 2012

@author: Yi
'''

from utils import searchEngine
from decorator import exception_handled
from merger import *
from tools import *
from rules import process_meta
from validates import validate_meta
import logging

_LOGGER = logging.getLogger("importer")

@exception_handled(logger = _LOGGER)
def metaImport(metaDup):

    # step 1 extract Meta
    metaDup = extractMeta(metaDup)

    if not metaDup:
        return None

    # step 2 process rules
    metaDup = process_meta(metaDup)

    _artist_name    = metaDup['artist']['name']
    _album_name     = metaDup['album']['name']
    _song_name      = metaDup['song']['name']

    # step 3 validate
    if not validate_meta(metaDup):
        return None

    # step 4 query
    _queryStr = "%s %s %s" % (_artist_name, _album_name, _song_name)

    _SEARCH_RESULTS = searchEngine.search(_queryStr)

    if not len(_SEARCH_RESULTS):
        _queryStr = "%s %s" % (_artist_name, _album_name)
        _SEARCH_RESULTS = searchEngine.search(_queryStr)

    if not len(_SEARCH_RESULTS):
        _queryStr = "%s" % (_artist_name)
        _SEARCH_RESULTS = searchEngine.search(_queryStr)

    # step 5 sorted the results
    _SEARCH_RESULTS = sorted(_SEARCH_RESULTS, key=lambda x: (-(x['artist']['name'] == _artist_name), -(x['album']['name'] == _album_name), -(x['song']['name'] == _song_name)))

    # step 6 match & merge
    meta = None

    for _meta in _SEARCH_RESULTS[:1]:
        meta = _meta

    matchType = matchMeta(meta, metaDup)

    _LOGGER.info('<%d, %d><%s %s %s>' % (len(_SEARCH_RESULTS), matchType, _artist_name, _album_name, _song_name))

    mergedMeta = mergeMeta(meta, metaDup, matchType)

    if mergedMeta and matchType not in [MatchType.III]:
        searchEngine.add({
            'song_id': mergedMeta['song']['id'],
            'name': _song_name,
            'album_name': _album_name,
            'artist_name': _artist_name
            })

    return mergedMeta
