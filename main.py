import requests
from bs4 import BeautifulSoup
import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('뉴스기사 스크래핑 시작')



# def crawler_melon():
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
  }
req = requests.get('https://www.melon.com/chart/week/index.htm', headers=header)
html = req.text
parse = BeautifulSoup(html, 'html.parser')

titles = parse.find_all("div", "ellipsis rank01")
singer = parse.find_all("span", "checkEllipsis")
song_detail = parse.find_all("a", "song_info")
album_detail = parse.find_all("a", "image_typeAll")

data = {
    'song': [],
    'songs_detail': [],
    'artist': [],
    'artist_detail': [],
    'thumbnail': [],
    'albums_detail': [],                
}

# song = []
# songs_detail = []
# artist = []
# artist_detail = []
# thumbnail = []
# albums_detail = []

for u in parse.select("span.checkEllipsis"):
    u = u.find('a')
    u = u.get('href')
    data['artist_detail'].append(u)

for sd in song_detail:
    sd = sd.get('href')
    data['songs_detail'].append(sd)

for ad in album_detail:
    ad = ad.get('href')
    data['albums_detail'].append(ad)

for t in titles:
    t = t.text.replace("\n", "")
    data['song'].append(t)

for s in singer:
    s=s.text.replace("\n", "")
    data['artist'].append(s)

for thumbs_img in parse.select(".image_typeAll"):
    thumbs_img = thumbs_img.find("img")
    thumbs_img = thumbs_img.get("src")
    data['thumbnail'].append(thumbs_img)

#   return [song, artist, thumbnail, artist_detail, songs_detail, albums_detail]
# result = crawler_melon()

with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii = False, indent='\t')

print('뉴스기사 스크래핑 끝')