  
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests, urllib, random, string, time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

THUMBNAIL = []

with open('request.txt', 'r', encoding='utf-8') as f:
    request_list = f.readlines()
item_list = [request.replace("\n", "") for request in request_list]
print(f"아이템 수량: {len(item_list)}")

with open('쇼핑몰.txt', 'w') as f:
    f.write('')

with open('img_error.txt', 'w') as f:
    f.write('')

driver = webdriver.Chrome(ChromeDriverManager().install())
xpath = By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[1]/li/div/div[1]/div/a/img'

def save_info(query):
    driver.get(f'https://search.shopping.naver.com/search/all?query={query} "{query}"&sort=review')
    time.sleep(0.5)
    html = driver.execute_script('return document.body.outerHTML;')
    soup = BeautifulSoup(html, 'html.parser')
    no_result = soup.find('div',{'class':'noResult_no_result__1ad0P'})
    rated = soup.find_all("p", string="연령 확인이 필요한 서비스입니다. 로그인후 이용해 주세요.")
    price = soup.find('div', {'class': 'basicList_price_area__1UXXR'})

    if no_result:
        no_result_list = ["No Result" for i in range(0,5)]
        row = [query] + no_result_list
    elif rated:
        rated_list = ["청소년 부적절" for i in range(0,5)]
        row = [query] + rated_list
    elif price:
        price = price.text
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
                mall_name = mall_name.find('img')['alt']
            else:
                mall_name = mall_name.text
        date = soup.find('button', {'class': 'basicList_btn_zzim__2MGkM'}).parent.previous_sibling.text.replace('등록일 ','')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        img_name= f"{current_time}-{random_code}"
        row = [query, price, cat, review, mall_name, date, img_name]
        thumbnail = soup.find('a', {'class': 'thumbnail_thumb__3Agq6'})
        if thumbnail:
            try:
                thumbnail = thumbnail.find('img')['src'].split("?type")[0]
            except TypeError:
                try:
                    driver.refresh()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(xpath))
                except TimeoutError:
                    with open('bug_report.txt' ,'a', encoding='utf-8') as f:
                        f.write(f"{query}\n")
                    return
                thumbnail = soup.find('a', {'class': 'thumbnail_thumb__3Agq6'}).find('img')['src'].split("?type")[0]
            urllib.request.urlretrieve(thumbnail, f'images/{img_name}.jpg')
    
    else:
        with open('bug_report.txt' ,'a', encoding='utf-8') as f:
            f.write(f"{query}\n")
        return
    
    row = ('\t').join(row)
    with open('쇼핑몰.txt', 'a', encoding='utf-8') as f:
        f.write(f"{row}\n")

for item in item_list:
    save_info(item)
    print(f"완료된 요청 수: {item_list.index(item)+1}/{len(item_list)}---{item}")
driver.quit()

root=tk.Tk()
root.withdraw()
messagebox.showinfo('info','크롤링 완료')