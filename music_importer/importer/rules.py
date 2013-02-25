import re, HTMLParser

def process_song(song):
    for rule in RULES:
        song = rule().process_song(song)
    return song

def process_album(album):
    for rule in RULES:
        album = rule().process_album(album)
    return album

def process_artist(artist):
    for rule in RULES:
        artist = rule().process_artist(artist)
    return artist

def process_meta(meta):
    for rule in RULES:
        rule().process_artist(meta['artist'])
        rule().process_album(meta['album'])
        rule().process_song(meta['song'])
    return meta

class Rule(object):

    def process_song(self, song):
        return song

    def process_album(self, album):
        return album

    def process_artist(self, artist):
        return artist

class UnescapeRule(Rule):

    def process_song(self, song):
        song['name'] = HTMLParser.HTMLParser().unescape(song['name'])
        return song

    def process_album(self, album):
        album['name'] = HTMLParser.HTMLParser().unescape(album['name'])
        return album

    def process_artist(self, artist):
        artist['name'] = HTMLParser.HTMLParser().unescape(artist['name'])
        return artist

class BoundaryRule(Rule):

    def process_song(self, song):
        if song['rank'] < 0:
            song['rank'] = 0
        elif song['rank'] > 100:
            song['rank'] = 100
        return song

    def process_album(self, album):
        if album['rank'] < 0:
            album['rank'] = 0
        elif album['rank'] > 100:
            album['rank'] = 100
        return album

    def process_artist(self, artist):
        if artist['rank'] < 0:
            artist['rank'] = 0
        elif artist['rank'] > 100:
            artist['rank'] = 100
        return artist

class CleanTextRule(Rule):

    def process_song(self, song):
        return song

    def process_album(self, album):
        return album

    def process_artist(self, artist):
        return artist

RULES = [CleanTextRule, BoundaryRule, UnescapeRule]
