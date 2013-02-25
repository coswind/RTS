# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_importer.settings")

# from utils.rabbitmq import MQType, send_message

# import json, pika

# meta = {
#     'artist': {
#         'name': 'import-ar-delta2',
#     },
#     'album': {
#         'name': 'import-al-delta2',
#     },
#     'song': {
#         'name': 'import-so-delta2',
#         'rank': 55,
#         'authority': 4,
#     },
#     'mp3': {
#         'fs_key': 'import-mp-delta2'
#     }
# }

# properties = pika.BasicProperties(content_type="application/json", delivery_mode = 2)
# send_message(MQType.NormalQueue, json.dumps(meta), properties)

from utils import searchEngine

# searchEngine.add({
#     'song_id': 1111,
#     'name': '夹子电动大乐队',
#     'album_name': '不会说台语',
#     'artist_name': '不会说台语'
#     })

print searchEngine.search('汪明荃 采茶山歌 采茶山歌(刘三姐)')
