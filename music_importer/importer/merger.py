'''
Created on Nov 1, 2012

@author: Yi
'''

from decorator import exception_handled
from tools import MatchType, merge_object, merge_extra, merge_field
from data.models import *
from data import meta_db
from utils import model2dct
import json, logging

_LOGGER = logging.getLogger("merger")

ARTIST_FIELDS = ['name', 'rank', 'authority', 'extra']
ALBUM_FIELDS = ['name', 'type', 'rank', 'authority', 'cover_url', 'genre', 'pubdate', 'extra']
SONG_FIELDS = ['name', 'duration', 'rank', 'authority', 'track', 'disc', 'lyrics', 'extra']

@exception_handled(logger = _LOGGER)
def mergeMeta(meta, metaDup, matchType = MatchType.OOO):

    if not metaDup:
        return None

    if not meta and not (matchType == MatchType.OOO):
        return None

    if matchType == MatchType.III:
        # merge artist
        artist = mergeArtist(meta['artist'], metaDup['artist'])
        # merge album
        album = mergeAlbum(meta['album'], metaDup['album'])
        # merge song
        song = mergeSong(meta['song'], metaDup['song'])
        # create mp3
        mp3 = createMp3(metaDup['mp3'], song.id)
    elif matchType == MatchType.IIO:
        artist = mergeArtist(meta['artist'], metaDup['artist'])
        album = mergeAlbum(meta['album'], metaDup['album'])
        song = createSong(metaDup['song'], artist.id, album.id)
        mp3 = createMp3(metaDup['mp3'], song.id)
    elif matchType in [MatchType.IOO, MatchType.IOI]:
        artist = mergeArtist(meta['artist'], metaDup['artist'])
        album = createAlbum(metaDup['album'], artist.id)
        song = createSong(metaDup['song'], artist.id, album.id)
        mp3 = createMp3(metaDup['mp3'], song.id)
    else:
        artist = createArtist(metaDup['artist'])
        album = createAlbum(metaDup['album'], artist.id)
        song = createSong(metaDup['song'], artist.id, album.id)
        mp3 = createMp3(metaDup['mp3'], song.id)

    return {
        'artist': model2dct(artist),
        'album': model2dct(album),
        'song': model2dct(song),
        'mp3': model2dct(mp3)
    }

def createMp3(metaMp3, song_id):
    mp3 = Mp3(song_id = song_id)
    save_data(mp3, metaMp3)
    return mp3

def createSong(metaSong, artist_id, album_id):
    song = Song(artist_id = artist_id, album_id = album_id)
    save_data(song, metaSong)
    return song

def createAlbum(metaAlbum, artist_id):
    album = Album(artist_id = artist_id)
    save_data(album, metaAlbum)
    return album

def createArtist(metaArtist):
    artist = Artist()
    save_data(artist, metaArtist)
    return artist

def mergeSong(song, songDup):
    # set overwrite
    overwrite = songDup['authority'] > song['authority']
    # merge fields
    merge_object(song, songDup, SONG_FIELDS, overwrite = overwrite)
    # merge extra
    song['extra'] = merge_extra(song['extra'], songDup['extra'], overwrite = overwrite)
    # save
    return save_data(meta_db.get_song(id = song['id']), song)

def mergeAlbum(album, albumDup):
    overwrite = albumDup['authority'] > album['authority']
    merge_object(album, albumDup, ALBUM_FIELDS, overwrite = overwrite)
    album['extra'] = merge_extra(album['extra'], albumDup['extra'], overwrite = overwrite)
    return save_data(meta_db.get_album(id = album['id']), album)

def mergeArtist(artist, artistDup):
    overwrite = artistDup['authority'] > artist['authority']
    merge_object(artist, artistDup, ARTIST_FIELDS, overwrite = overwrite)
    artist['extra'] = merge_extra(artist['extra'], artistDup['extra'], overwrite = overwrite)
    return save_data(meta_db.get_artist(id = artist['id']), artist)

def save_data(obj, cleaned_dict):
    for field in cleaned_dict:
        setattr(obj, field, cleaned_dict[field])
    obj.save()
    return obj
