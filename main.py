import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.melon.com/chart/day/index.htm'

req_header_dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
res = requests.get(url, headers=req_header_dict)

html = res.text

soup = BeautifulSoup(html, 'html.parser')
# lst50 > td:nth-child(4) > div > a > img
rank = 0
titles = soup.select('.rank01')
artists = soup.select('.checkEllipsis')
thumbs = soup.select('img')
albums = soup.select('.rank03')
song_ids = soup.select('.input_check ')
urls = 'https://www.melon.com/song/detail.htm?songId='

song_list = []
for title, artist, thumb, album, song_id in zip(titles, artists, thumbs, albums, song_ids):
    song_dict = {}
    rank = rank + 1
    title = title.text.strip()
    artist = artist.text
    album = album.text.strip()
    thumb = thumb.get('src')
    song_id = song_id.get('value')
    detail_url = f'https://www.melon.com/song/detail.htm?songId={song_id}'
    song_dict['순위'] = rank
    song_dict['곡명'] = title
    song_dict['가수'] = artist
    song_dict['앨범'] = album
    song_dict['재킷'] = thumb
    song_dict['상세정보'] = detail_url
    song_list.append(song_dict)

print(song_list)

with open('melonTop100.json', 'w', encoding='utf-8') as file:
    json.dump(song_list, file, ensure_ascii=False)
