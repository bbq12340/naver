# -*- coding: utf-8 -*- 
from naver_estates import extract_naver_estate
from datetime import datetime

with open('request.txt', 'r', encoding='utf-8') as f:
    request_list = f.readlines()
request_list = [request.replace("\n", "") for request in request_list]
print(f"요청 아이템 수량: {len(request_list)}")

for r in request_list:
    print(f"-------------------------------------------------\n검색어:{r}\n{request_list.index(r)+1}/{len(request_list)} 을 요청합니다.")
    print(f"현재 시각: {datetime.now()}\n-------------------------------------------------")
    extract_naver_estate(r)