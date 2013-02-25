'''
Created on Nov 2, 2012

@author: Yi
'''

from datetime import datetime
from django.utils.timezone import utc
import json

class MatchType(object):
    OOO = 0
    OOI = 1 #song match
    OIO = 2 #album match
    OII = 3
    IOO = 4 #artist match
    IOI = 5
    IIO = 6
    III = 7

def matchMeta(meta, metaDup):
    matched = MatchType.OOO

    if not meta or not metaDup:
        return matched

    matched |= MatchType.IOO if meta['artist']['name'] == metaDup['artist']['name'] else MatchType.OOO
    matched |= MatchType.OIO if meta['album']['name'] == metaDup['album']['name'] else MatchType.OOO
    matched |= MatchType.OOI if meta['song']['name'] == metaDup['song']['name'] else MatchType.OOO

    return matched

def extractMeta(meta):
    _META = None

    if not meta:
        return _META

    _artist     = meta.get('artist', {})
    _album      = meta.get('album', {})
    _song       = meta.get('song', {})
    _mp3        = meta.get('mp3', {})

    _META = {
        'artist': {
            'name':         _artist.get('name', ''),
            'rank':         _artist.get('rank', 0),
            'authority':    _artist.get('authority', 0),
            'extra':        _artist.get('extra', '{}')
        },
        'album': {
            'name':         _album.get('name', ''),
            'type':         _album.get('type', 0),
            'rank':         _album.get('rank', 0),
            'authority':    _album.get('authority', 0),
            'cover_url':    _album.get('cover_url', ''),
            'genre':        _album.get('genre', ''),
            'pubdate':      _album.get('pubdate', datetime.min.replace(tzinfo = utc)),
            'extra':        _album.get('extra', '{}')
        },
        'song': {
            'name':         _song.get('name', ''),
            'duration':     _song.get('duration', 0),
            'rank':         _song.get('rank', 0),
            'authority':    _song.get('authority', 0),
            'track':        _song.get('track', 0),
            'disc':         _song.get('disc', 0),
            'lyrics':       _song.get('lyrics', ''),
            'extra':        _song.get('extra', '{}'),
        },
        'mp3': {
            'authority':    _mp3.get('authority', 0),
            'similarity':   _mp3.get('similarity', 0),
            'fs_key':       _mp3.get('fs_key', ''),
            'extra':        _mp3.get('extra', '{}'),
        }
    }

    return _META

def merge_object(to_obj, from_obj, fields = [], overwrite = False):
    for field in fields:
        value = merge_field(to_obj.get(field), from_obj.get(field), overwrite)
        to_obj[field] = value

def merge_extra(extra, extra_new, overwrite = False):
    if not extra_new:
        return extra
    try:
        extra = json.loads(extra) if extra else {}
        extra_new = json.loads(extra_new)
    except:
        return '{}'
    for key in extra_new.keys():
        if not extra.has_key(key) or overwrite:
            extra[key] = extra_new[key]
    return json.dumps(extra)

def merge_field(oldvalue, newvalue, overwrite = False):
    if not newvalue:
        return oldvalue
    elif not oldvalue:
        return newvalue
    else:
        return newvalue if overwrite else oldvalue
