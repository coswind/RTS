from django.db import models
from datetime import datetime
from django.utils.timezone import utc

# Create your models here.

class Mp3(models.Model):
    class Meta:
        db_table = "mp3"
    id = models.AutoField(primary_key = True)
    uuid = models.CharField(max_length = 36, db_index = True, default = "")
    song_id = models.IntegerField(db_index = True)
    authority = models.SmallIntegerField(default = 0)
    similarity = models.FloatField(default = 0)
    fs_key = models.CharField(max_length = 255)
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

    def get_localpeak_fskey(self):
        return "localpeak_%d" % self.id

class MP3_i18n(models.Model):
    class Meta:
        db_table = "mp3_i18n"
    id = models.AutoField(primary_key = True)
    mp3_id = models.IntegerField(db_index = True)
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

class Song(models.Model):
    class Meta:
        db_table = 'song'
    id = models.AutoField(primary_key = True)
    uuid = models.CharField(max_length = 36, db_index = True, default = "")
    name = models.CharField(max_length = 255, default = "")
    artist_id = models.IntegerField(db_index = True, default = 0)
    album_id = models.IntegerField(db_index = True, default = 0)
    duration = models.SmallIntegerField(default = 0)
    rank = models.SmallIntegerField(default = 0)
    authority = models.SmallIntegerField(default = 0)
    track = models.SmallIntegerField(default = 0)
    disc = models.SmallIntegerField(default = 0)
    lyrics = models.TextField(default = "")
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

    def get_album(self):
        if not self.album_id:
            return None
        try:
            return Album.objects.get(id = self.album_id)
        except Album.DoesNotExist:
            return None

    def get_artist(self):
        if not self.artist_id:
            return None
        try:
            return Artist.objects.get(id = self.artist_id)
        except Artist.DoesNotExist:
            return None

class Song_i18n(models.Model):
    class Meta:
        db_table = "song_i18n"
    id = models.AutoField(primary_key = True)
    song_id = models.IntegerField(db_index = True)
    lang = models.CharField(max_length = 255, default = "")
    name = models.CharField(max_length = 255, default = "")
    lyrics = models.TextField(default = "")
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

class Album(models.Model):
    class Meta:
        db_table = 'album'
    id = models.AutoField(primary_key = True)
    uuid = models.CharField(max_length = 36, db_index = True, default = "")
    name = models.CharField(max_length = 255, default = "")
    type = models.SmallIntegerField(default = 0)
    artist_id = models.IntegerField(db_index = True, default = 0)
    rank = models.SmallIntegerField(default = 0)
    authority = models.SmallIntegerField(default = 0)
    cover_url = models.CharField(max_length = 1024, default = "")
    genre = models.CharField(max_length = 255, default = "")
    pubdate = models.DateTimeField(default = datetime.min.replace(tzinfo = utc))
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

    def get_artist(self):
        if not self.artist_id:
            return None
        try:
            return Artist.objects.get(id = self.artist_id)
        except Artist.DoesNotExist:
            return None

class Album_i18n(models.Model):
    class Meta:
        db_table = "album_i18n"
    id = models.AutoField(primary_key = True)
    album_id = models.IntegerField(db_index = True)
    lang = models.CharField(max_length = 255, default = "")
    name = models.CharField(max_length = 255, default = "")
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

class Artist(models.Model):
    class Meta:
        db_table = 'artist'
    id = models.AutoField(primary_key = True)
    uuid = models.CharField(max_length = 36, db_index = True, default = "")
    name = models.CharField(max_length = 255, default = "")
    rank = models.IntegerField(default = 0)
    authority = models.SmallIntegerField(default = 0)
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

class Artist_i18n(models.Model):
    class Meta:
        db_table = "artist_i18n"
    id = models.AutoField(primary_key = True)
    artist_id = models.IntegerField(db_index = True)
    lang = models.CharField(max_length = 255, default = "")
    name = models.CharField(max_length = 255, default = "")
    extra = models.TextField(default = "{}")
    created_dt = models.DateTimeField(default = datetime.now().replace(tzinfo = utc))
    updated_dt = models.DateTimeField(auto_now = True, auto_now_add = True)

class FSEntry(models.Model):
    class Meta:
        db_table = "fs_entry"
    key = models.CharField(max_length = 255, primary_key = True)
    vol_id = models.SmallIntegerField()
    md5 = models.CharField(max_length = 32, db_index = True)

class FSEntryAmazon(models.Model):
    class Meta:
        db_table = "fs_entry_amazon"
    key = models.CharField(max_length = 255, primary_key = True)
    vol_id = models.SmallIntegerField()
    md5 = models.CharField(max_length = 32, db_index = True)

class FSVol(models.Model):
    class Meta:
        db_table = 'fs_vol'
    id = models.SmallIntegerField(primary_key = True)
    total_bytes = models.BigIntegerField(default = 850 * 1024 * 1024 * 1024)
    used_bytes = models.BigIntegerField(default = 0)
    writable = models.BooleanField(default = True, db_index = True)
    rule = models.CharField(max_length = 255, db_index = True, default = 'default')
