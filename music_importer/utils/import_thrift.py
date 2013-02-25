# -*- coding: utf-8 -*-
from decorator import thrift_call

from thrift_service import SearchService
from thrift_service.ttypes import *

THRIFT_SERVER = ('127.0.0.1', 9090)

def wrap_import_service_result(retval):
    return retval

import_service_thrift_call = thrift_call(thrift_server = THRIFT_SERVER,
                                        client_cls = SearchService.Client,
                                        result_cls = wrap_import_service_result
                                        )

@import_service_thrift_call
def addDoc(meta = None, thrift_client = None):
    result = 0
    if meta:
        metaBean = MetaBean(
                    song_id = meta['song_id'],
                    name = unicode2Str(meta['name']),
                    album_name = unicode2Str(meta['album_name']),
                    artist_name = unicode2Str(meta['artist_name']),
                )
        result = thrift_client.addDoc(metaBean)
    return result

@import_service_thrift_call
def searchDoc(query = None, thrift_client = None):
    result = []
    if query:
        query = unicode2Str(query)
        result = thrift_client.search(query)
    return result

def unicode2Str(text):
    if type(text) == unicode:
        text = text.encode('utf-8')

    return text
