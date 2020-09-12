  
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests, urllib, random, string
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import tkinter as tk


with open('request.txt', 'r', encoding='utf-8') as f:
    request_list = f.readlines()
item_list = [request.replace("\n", "") for request in request_list]
print(f"아이템 수량: {len(item_list)}")

"""
def open_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver
"""
def save_info(query):
    r = requests.get(f'https://search.shopping.naver.com/search/all?query={query} "{query}"&sort=review')
    soup = BeautifulSoup(r.text, 'html.parser')
    no_result = soup.find('div',{'class':'noResult_no_result__1ad0P'})

    if no_result:
        price = "No Result"
        cat = "No Result"
        review = "No Result"
    elif soup.find_all(text="연령 확인이 필요한 서비스입니다. 로그인후 이용해 주세요."):
        price = "청소년 부적절"
        cat = "청소년 부적절"
        review = "청소년 부적절"
    else:
        price = soup.find('div', {'class': 'basicList_price_area__1UXXR'}).text
        category = soup.find('div', {'class': 'basicList_depth__2QIie'})
        li = category.find_all('a')
        a_tags = [a.text for a in li]
        cat = ">".join(a_tags)
        try:
            review = soup.select_one('.basicList_num__1yXM9').text
        except:
            review = 0
        mall_area = soup.find('div', {'class': 'basicList_mall_area__lIA7R'})
        mall_list = mall_area.find('ul', {'class': 'basicList_mall_list__vIiQw'})
        if mall_list:
            mall_name = mall_list.find('span', {'class': 'basicList_mall_name__1XaKA'}).text
        else:
            mall_name = mall_area.find('div', {'class': 'basicList_mall_title__3MWFY'}).find('a')
            if mall_name.find('img'):
                mall_name = mall_name['alt']
            else:
                mall_name = mall_name.text
        date = soup.find('button', {'class': 'basicList_btn_zzim__2MGkM'}).parent.previous_sibling.text.replace('등록일 ','')
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d %H:%M:%S")
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        img_name= f"{current_time}-{random_code}"
        row = [query, price, cat, review, mall_name, date, img_name]
        #thumbnail = soup.find('a', {'class': 'thumbnail_thumb__3Agq6'})

        with open('html.txt', 'w') as f:
            f.write(str(soup))
        """
        try:
            urllib.request.urlretrieve(thumbnail, f"{img_name}.jpg")
        except Exception:
            with open("img_error.txt", 'a', encoding='utf-8') as f:
                f.write(f"thumbnail\n")
        """
        with open('쇼핑몰.txt', 'a', encoding='utf-8'):
            row = ('\t').join(row)
            f.writelines(row)
        



for item in item_list:
    save_info(item)
    print(f"완료된 요청 수: {item_list.index(item)+1}/{len(item_list)}")

root=tk.Tk()
root.withdraw()
messagebox.showinfo('info','크롤링 완료')