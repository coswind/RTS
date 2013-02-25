'''
Created on Nov 1, 2012

@author: Yi
'''

from utils import model2dct
from models import *
import logging

_LOGGER = logging.getLogger("meta_db")

def get_meta(song_id):
    if not song_id:
        return None
    try:
        mp3s = Mp3.objects.filter(song_id = song_id)
        song = Song.objects.get(id = song_id)
        album = Album.objects.get(id = song.album_id)
        artist = Artist.objects.get(id = song.artist_id)
        return {
            'artist': model2dct(artist),
            'album': model2dct(album),
            'song': model2dct(song),
            'mp3': map((lambda mp3: model2dct(mp3)), mp3s)
        }
    except Exception, e:
        _LOGGER.error('Error while get_meta from song_id %d\n %s.', song_id, str(e))
        return None

def get_meta_by_mp3(mp3_id):
    if not mp3_id:
        return None
    try:
        mp3 = Mp3.objects.get(id = mp3_id)
        song = Song.objects.get(id = mp3.song_id)
        album = Album.objects.get(id = song.album_id)
        artist = Artist.objects.get(id = song.artist_id)
        return {
            'artist': model2dct(artist),
            'album': model2dct(album),
            'song': model2dct(song),
            'mp3': model2dct(mp3),
        }
    except Exception, e:
        _LOGGER.error('Error while get_meta from mp3_id %d\n %s.', mp3_id, str(e))
        return None

def get_song(id):
    if not id:
        return None
    try:
        return Song.objects.get(id = id)
    except Song.DoesNotExist:
        return None

def get_album(id):
    if not id:
        return None
    try:
        return Album.objects.get(id = id)
    except Album.DoesNotExist:
        return None

def get_artist(id):
    if not id:
        return None
    try:
        return Artist.objects.get(id = id)
    except Artist.DoesNotExist:
        return None

def get_mp3(id):
    if not id:
        return None
    try:
        return Mp3.objects.get(id = id)
    except Mp3.DoesNotExist:
        return None
