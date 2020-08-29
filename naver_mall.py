  
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
import tkinter as tk

PRICE = []
CATEGORY = []
REVIEW = []

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
    with open('results/가격.txt', 'a', encoding='utf-8') as f:
        f.write(f"{price}\n")
    with open('results/카테고리.txt', 'a', encoding='utf-8') as f:
        f.write(f"{cat}\n")
    with open('results/리뷰.txt', 'a', encoding='utf-8') as f:
        f.write(f"{review}\n")


for item in item_list:
    save_info(item)
    print(f"완료된 요청 수: {item_list.index(item)+1}/{len(item_list)}")

root=tk.Tk()
root.withdraw()
messagebox.showinfo('info','크롤링 완료')