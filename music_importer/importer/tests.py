"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from data import meta_db
from merger import *
from tools import *
from data.models import *
from importer import metaImport

from utils import model2dct

from datetime import datetime
from django.utils.timezone import utc

class CreateTest(unittest.TestCase):
    def test_create_case(self):
        meta = {
            'artist': {
                'name': 'create-ar',
            },
            'album': {
                'name': 'create-al',
            },
            'song': {
                'name': 'create-so'
            },
            'mp3': {
                'fs_key': 'create-mp'
            }
        }
        artist = createArtist(meta['artist'])
        album = createAlbum(meta['album'], artist.id)
        song = createSong(meta['song'], artist.id, album.id)

        self.assertEqual(album.name, meta['album']['name'])
        self.assertEqual(artist.name, meta['artist']['name'])
        self.assertEqual(song.name, meta['song']['name'])

class MergeTest(unittest.TestCase):
    def setUp(self):
        self.meta = {
            'artist': {
                'name': 'merge-ar',
            },
            'album': {
                'name': 'merge-al',
            },
            'song': {
                'name': 'merge-so'
            },
            'mp3': {
                'fs_key': 'merge-mp'
            }
        }
        self.metaDup = extractMeta({
            'artist': {
                'name': 'merge-ar-dup',
                'authority': 0,
            },
            'album': {
                'name': 'merge-al-dup',
                'authority': 1,
            },
            'song': {
                'name': 'merge-so-dup',
                'authority': 1,
            },
            'mp3': {
                'fs_key': 'merge-mp-dup'
            }
        })
        self.artist = createArtist(self.meta['artist'])
        self.album = createAlbum(self.meta['album'], self.artist.id)
        self.song = createSong(self.meta['song'], self.artist.id, self.album.id)

    def test_merge_case(self):
        artist = mergeArtist(model2dct(self.artist), self.metaDup['artist'])
        album = mergeAlbum(model2dct(self.album), self.metaDup['album'])
        song = mergeSong(model2dct(self.song), self.metaDup['song'])

        self.assertEqual(artist.name, self.meta['artist']['name'])
        self.assertEqual(album.name, self.metaDup['album']['name'])
        self.assertEqual(song.name, self.metaDup['song']['name'])

class MergeMetaTest(unittest.TestCase):
    def test_mergeOOO_case(self):
        metaDup = extractMeta({
            'artist': {
                'name': 'meta-ar-dup-OOO',
            },
            'album': {
                'name': 'meta-al-dup-OOO',
            },
            'song': {
                'name': 'meta-so-dup-OOO',
            },
            'mp3': {
                'fs_key': 'meta-mp-dup-OOO'
            }
        })

        metaResult = mergeMeta(None, metaDup, MatchType.OOO)
        metaResult = meta_db.get_meta_by_mp3(metaResult['mp3']['id'])

        self.assertEqual(metaResult['artist']['name'], metaDup['artist']['name'])
        self.assertEqual(metaResult['album']['name'], metaDup['album']['name'])
        self.assertEqual(metaResult['song']['name'], metaDup['song']['name'])
        self.assertEqual(metaResult['mp3']['fs_key'], metaDup['mp3']['fs_key'])

    def test_mergeIOO_case(self):
        meta = extractMeta({
            'artist': {
                'name': 'meta-ar-IOO',
            },
            'album': {
                'name': 'meta-al-IOO',
            },
            'song': {
                'name': 'meta-so-IOO'
            },
            'mp3': {
                'fs_key': 'meta-mp-IOO'
            }
        })
        metaDup = extractMeta({
            'artist': {
                'name': 'meta-ar-IOO',
            },
            'album': {
                'name': 'meta-al-dup-IOO',
            },
            'song': {
                'name': 'meta-so-dup-IOO',
            },
            'mp3': {
                'fs_key': 'meta-mp-dup-IOO'
            }
        })

        artist = createArtist(meta['artist'])
        album = createAlbum(meta['album'], artist.id)
        song = createSong(meta['song'], artist.id, album.id)
        createMp3(meta['mp3'], song.id)

        meta = meta_db.get_meta(song.id)

        metaResult = mergeMeta(meta, metaDup, MatchType.IOO)
        metaResult = meta_db.get_meta_by_mp3(metaResult['mp3']['id'])

        self.assertEqual(metaResult['artist']['name'], metaDup['artist']['name'])
        self.assertEqual(metaResult['album']['name'], metaDup['album']['name'])
        self.assertEqual(metaResult['song']['name'], metaDup['song']['name'])
        self.assertEqual(metaResult['mp3']['fs_key'], metaDup['mp3']['fs_key'])

    def test_mergeIIO_case(self):
        meta = extractMeta({
            'artist': {
                'name': 'meta-ar-IIO',
            },
            'album': {
                'name': 'meta-al-IIO',
            },
            'song': {
                'name': 'meta-so-IIO'
            },
            'mp3': {
                'fs_key': 'meta-mp-IIO'
            }
        })
        metaDup = extractMeta({
            'artist': {
                'name': 'meta-ar-IIO',
            },
            'album': {
                'name': 'meta-al-IIO',
            },
            'song': {
                'name': 'meta-so-dup-IIO',
            },
            'mp3': {
                'fs_key': 'meta-mp-dup-IIO'
            }
        })

        artist = createArtist(meta['artist'])
        album = createAlbum(meta['album'], artist.id)
        song = createSong(meta['song'], artist.id, album.id)
        createMp3(meta['mp3'], song.id)

        meta = meta_db.get_meta(song.id)

        metaResult = mergeMeta(meta, metaDup, MatchType.IIO)
        metaResult = meta_db.get_meta_by_mp3(metaResult['mp3']['id'])

        self.assertEqual(metaResult['artist']['name'], metaDup['artist']['name'])
        self.assertEqual(metaResult['album']['name'], metaDup['album']['name'])
        self.assertEqual(metaResult['song']['name'], metaDup['song']['name'])
        self.assertEqual(metaResult['mp3']['fs_key'], metaDup['mp3']['fs_key'])

    def test_mergeIII_case(self):
        meta = extractMeta({
            'artist': {
                'name': 'meta-ar-III',
            },
            'album': {
                'name': 'meta-al-III',
            },
            'song': {
                'name': 'meta-so-III'
            },
            'mp3': {
                'fs_key': 'meta-mp-III'
            }
        })
        metaDup = extractMeta({
            'artist': {
                'name': 'meta-ar-III',
            },
            'album': {
                'name': 'meta-al-III',
            },
            'song': {
                'name': 'meta-so-III',
            },
            'mp3': {
                'fs_key': 'meta-mp-dup-III'
            }
        })

        artist = createArtist(meta['artist'])
        album = createAlbum(meta['album'], artist.id)
        song = createSong(meta['song'], artist.id, album.id)
        createMp3(meta['mp3'], song.id)

        meta = meta_db.get_meta(song.id)

        metaResult = mergeMeta(meta, metaDup, MatchType.III)
        metaResult = meta_db.get_meta_by_mp3(metaResult['mp3']['id'])

        self.assertEqual(metaResult['artist']['name'], metaDup['artist']['name'])
        self.assertEqual(metaResult['album']['name'], metaDup['album']['name'])
        self.assertEqual(metaResult['song']['name'], metaDup['song']['name'])
        self.assertEqual(metaResult['mp3']['fs_key'], metaDup['mp3']['fs_key'])

class ImportMetaTest(unittest.TestCase):
    def test_import_case(self):
        meta = {
            'artist': {
                'name': 'import-ar',
            },
            'album': {
                'name': 'import-al',
            },
            'song': {
                'name': 'import-so'
            },
            'mp3': {
                'fs_key': 'import-mp'
            }
        }

        metaResult = metaImport(meta)
        metaResult = meta_db.get_meta_by_mp3(metaResult['mp3']['id'])

        self.assertEqual(metaResult['artist']['name'], meta['artist']['name'])
        self.assertEqual(metaResult['album']['name'], meta['album']['name'])
        self.assertEqual(metaResult['song']['name'], meta['song']['name'])
        self.assertEqual(metaResult['mp3']['fs_key'], meta['mp3']['fs_key'])
