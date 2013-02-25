'''
Created on Nov 1, 2012

@author: Yi
'''

from sphinxapi import *
from data import meta_db
from decorator import exception_handled
import logging

_LOGGER = logging.getLogger("search")

# HOST        = 'localhost'
# PORT        = 9312
# INDEX       = '*'
# LIMIT       = 20
# MODE        = SPH_MATCH_ALL

# # query settings
# _SCLIENT = SphinxClient()
# _SCLIENT.SetServer(HOST, PORT)

# @exception_handled(logger = _LOGGER)
# def search(query = None, limit = LIMIT, index = INDEX, searchMode = MODE):
#     # set conditions
#     _SCLIENT.SetLimits(0, limit)
#     _SCLIENT.SetMatchMode(searchMode)

#     # query index
#     _RESULT = _SCLIENT.Query(query, index)

#     _METAS = []

#     if not _RESULT:
#         return _METAS

#     if _RESULT.has_key('matches'):
#         for match in _RESULT['matches']:
#             id = match['id']
#             meta = meta_db.get_meta(id)
#             if meta:
#                 _METAS.append(meta)

#     return _METAS

from utils.import_thrift import *
from time import time

@exception_handled(logger = _LOGGER)
def search(query = None):
    _METAS = []
    _RESULT = []

    if not query:
        return _METAS

    startTime = time()

    _RESULT = searchDoc(query)

    _LOGGER.info('<%f> <%d> %s' % ((time() - startTime), len(_RESULT), query))

    for match in _RESULT:
        song_id = match.song_id
        meta = meta_db.get_meta(song_id)
        if meta:
            _METAS.append(meta)

    return _METAS

@exception_handled(logger = _LOGGER)
def add(meta = None):

    if meta:
        addDoc({
            'song_id': meta['song_id'],
            'name': meta['name'],
            'album_name': meta['album_name'],
            'artist_name': meta['artist_name']
            })

    return
