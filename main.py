import requests
from bs4 import BeautifulSoup
import re
import json
import time

from datetime import datetime, timezone


newTime = datetime.now()
# print(newTime)
dtString = newTime.strftime("%y_%m_%d_%H oclock")

period = ['day/', 'week/', 'month/']  # 일간, 주간, 월간


url = 'https://www.melon.com/chart/'+period[1]+'index.htm'
# print(url)
req_header_dict = {
    # 요청헤더 : 브라우저정보
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
res = requests.get(url, headers=req_header_dict)


if res.ok:
    html = res.text
    # html 전체 소스보기
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # html parsing
    # print(soup)

    # parsing한 html중 곡 에대한 정보를 담음 태그만 조회!!
a_tags = soup.select("div#tb_list tr a[href*='playSong']")
# print(a_tags)

song_list = []

for idx, a_tag in enumerate(a_tags, 1):
    # 노래 1곡의 정보를 저장할 dict 선언
    song_dict = {}
    # 노래 제목 갖고오기 <a href="">노래제목</a>
    song_title = a_tag.text
    # song_dict['rank'] = idx
    song_dict['song_title'] = song_title
    # print(song_dict)

    # a태그의 href 속성의 값을 추출하기 javascript:melon.play.playSong('1000002721',34535898);
    href_value = a_tag['href']
    # print(href_value)
    # Song ID를 찾기 위한 정규표현식
    matched = re.search(r'(\d+)\);', href_value)
    # print(matched)
    if matched:
        # group(0) : 34535898);  group(1) : 34535898
        song_id = matched.group(1)
        song_dict['song_id'] = song_id

        song_detail_url = f'https://www.melon.com/song/lyrics.htm?songId={song_id}'
        song_dict['song_detail_url'] = song_detail_url
        song_list.append(song_dict)
        # print(song_list)

song_detail_list = []
# 결과가 매번 100개씩출력되어서 3순위까지 임시로 슬라이싱
for idx, song in enumerate(song_list, 1):
    # 노래 1곡의 상세정보를 저장할 dict
    song_detail_dict = {}
    song_detail_url = song['song_detail_url']
    # print(song_detail_url)

    res = requests.get(song_detail_url, headers=req_header_dict)
    # print(res.status_code)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(idx,song['song_title'])
        song_detail_dict['곡명'] = song['song_title']
        # 노래 1곡의 상세정보에 '곡명'을 찾아 주었다.
        # 다음으로 상세정보 '가수'를 찾는다
        singer = soup.select("a[href*='goArtistDetail'] span")
        # print(singer)
        if singer:
            # singer리스트에서 0번째 순서에 해당하는것을 text로 뽑으면 이름이다.
            song_detail_dict['가수'] = singer[0].text
        # print(singer[0].text)

        # 다음으로 div.meta에서 dd로 끝나는 값들을 넣어준다
        song_di = soup.select("div.meta dd")
        song_coverImg = soup.select_one(
            "#downloadfrm > div > div > div.thumb > a > img")['src']

        if song_di:
            song_detail_dict['앨범'] = song_di[0].text
            song_detail_dict['발매일'] = song_di[1].text
            song_detail_dict['장르'] = song_di[2].text
            song_detail_dict['FLAC'] = song_di[3].text
        song_detail_dict['상세정보'] = song_detail_url
        song_detail_dict['재킷'] = song_coverImg
        song_detail_dict['순위'] = idx
        song_detail_list.append(song_detail_dict)

print(song_detail_list)

with open('melonTop100.json', 'w', encoding='utf-8') as file:
    json.dump(song_detail_list, file, ensure_ascii=False)
