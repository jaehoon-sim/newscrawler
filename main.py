import requests
from bs4 import BeautifulSoup
import re
import json
import time

crtTime = time.localtime(time.time())
zoneTime = (f"{crtTime.tm_mon}.{crtTime.tm_mday}.{crtTime.tm_hour}.{crtTime.tm_min}")
print(zoneTime)
url = 'https://www.melon.com/chart/index.htm'
req_header_dict = {
    # 요청헤더 : 브라우저정보
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
res = requests.get(url, headers=req_header_dict)


if res.ok:
    html = res.text
    #html 전체 소스보기
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    #html parsing
    #print(soup)
    
    #parsing한 html중 곡 에대한 정보를 담음 태그만 조회!!
a_tags = soup.select("div#tb_list tr a[href*='playSong']")
#print(a_tags)

song_list = []

for idx, a_tag in enumerate(a_tags,1):
    #노래 1곡의 정보를 저장할 dict 선언 
    song_dict = {}    
    #노래 제목 갖고오기 <a href="">노래제목</a>
    song_title = a_tag.text
    song_dict['rank'] = idx
    song_dict['song_title'] = song_title
    # print(song_dict)
    
    
    #a태그의 href 속성의 값을 추출하기 javascript:melon.play.playSong('1000002721',34535898);
    href_value = a_tag['href']
    # print(href_value)
    #Song ID를 찾기 위한 정규표현식
    matched = re.search(r'(\d+)\);', href_value)
    # print(matched)
    if matched:
        song_id = matched.group(1) # group(0) : 34535898);  group(1) : 34535898
        song_dict['song_id'] = song_id
        print(song_title +" / " + song_id)
        
        song_detail_url = f'https://www.melon.com/song/detail.htm?songId={song_id}'
        song_dict['song_detail_url'] = song_detail_url
        song_list.append(song_dict)
        # print(song_list)

with open(f'melonTop100.{zoneTime}.json','w',encoding='utf-8') as file:
	json.dump(song_list, file, ensure_ascii=False)
