from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import time, datetime
import pandas as pd
import numpy as np

from browser import open_estate

def more_tab_condition(browser, query):
    if len(browser.window_handles)>1:
            browser.switch_to_window(browser.window_handles[-1])
            url = browser.current_url
            with open (f'네이버 외 부동산-{query}-{datetime.date.today()}.txt', 'a') as f:
                f.write(f"{url}\n")
            browser.close()
            browser.switch_to_window(browser.window_handles[0])

def clean_data(query):
    print('데이터 정리 중...')
    date = datetime.date.today()
    df = pd.read_csv(f'{query}.csv', index_col=0)
    cleaned_df = df.drop_duplicates(subset=['매물 번호'])
    diff = len(df.index) - len(cleaned_df)
    cleaned_df.to_excel(f'{query}-{date}.xlsx', encoding='utf-8')
    print(f'{diff} 만큼의 중복 데이터가 처리되었습니다.')

def scroll_item_list(query):
    browser = open_estate(query)
    wait = WebDriverWait(browser, 30)
    ITEM_BY_CLASS = By.CLASS_NAME, 'item_link'
    wait.until(EC.element_to_be_clickable(ITEM_BY_CLASS))
    item_list = 'document.querySelector(".item_list")'
    print(f"{query} 스크롤 중...")
    while True:
        browser.execute_script(f'{item_list}.scrollTo({item_list}.scrollTop, {item_list}.scrollHeight);')
        try:
            browser.find_element_by_class_name("loader")
            continue
        except NoSuchElementException:
            break
    return browser
def extract_naver_estate(query):
    ITEM_TABLE_BY_CLASS = By.CLASS_NAME, 'info_table_wrap'
    browser = scroll_item_list(query)
    wait = WebDriverWait(browser, 30) 
    items = browser.find_elements_by_class_name('item_link')
    print(f'총 아이템 수: {len(items)}')
    df = pd.DataFrame([], columns=['매물 번호','매물유형', '매물명', '날짜', '층', '매물 특징', '거래방식', '가격', '평당금액(만원)', '계약 면적(평)', '전용 면적(평)', '대지 면적(평)', '연 면적(평)', '링크'])
    items[0].click()
    more_tab_condition(browser, query)
    browser.execute_script('document.querySelector(".tab_area_unit").click();')
    for item in items:
        print(f"{items.index(item)+1}/{len(items)} 진행완료")
        item.click()
        more_tab_condition(browser, query)
            
        
        wait.until(EC.presence_of_element_located(ITEM_TABLE_BY_CLASS))
        html = browser.execute_script("return document.querySelector('.detail_contents_inner').outerHTML")
        soup = BeautifulSoup(html, 'html.parser')

        url = browser.current_url
        num = soup.find('th', text='매물번호').next_sibling.text
        category = soup.find('span', {'class': 'label--category'}).text
        title = soup.find('h4',{'class':'info_title'}).text
        date = soup.find('span', {'class': 'label'}).text
        if category == '토지':
            floor = np.nan
        else:
            floor = soup.find('span', {'class': 'feature'}).text
        feature = soup.find('td', {'class': 'table_td'}).text
        trade_type = soup.find('span', {'class': 'type'}).text
        space = soup.find_all('span', {'class': 'feature'})[-1].text.split(':')[-1].split('/')
        space_type = soup.find_all('span', {'class': 'feature'})[-1].text.split(':')[0]
        contract_space = space[0].replace('평','')
        whole_space = space[-1].replace('평','')  
        price = soup.find('span', {'class': 'price'}).text
        price_pyeong = soup.find('span',{'class': 'price_per-pyeong'})
        if price_pyeong:
            price_pyeong = price_pyeong.text.split('/')[0].replace('(','').replace('만원','').replace(',','')
        elif category == '창고':
            try:
                price_pyeong_1 = float(price.split('/')[-1].replace(',',''))/float(contract_space)
                price_pyeong_1 = round(price_pyeong_1,2)
                price_pyeong_2 = float(price.split('/')[-1].replace(',',''))/float(whole_space)
                price_pyeong_2 = round(price_pyeong_2,2)
                price_pyeong = price_pyeong_1+'/'+price_pyeong_2
            except ValueError:
                string_value = price.split('/')[-1].replace(',','').split(" ")
                float_value = float(string_value[0].replace('억', '00000000')) + float(string_value[1])
                price_pyeong_1 = round(float_value/float(contract_space), 2)
                price_pyeong_2 = round(float_value/float(whole_space) ,2)
                price_pyeong = price_pyeong_1+'/'+price_pyeong_2
        else:
            try:
                price_pyeong = float(price.split('/')[-1].replace(',',''))/float(contract_space)
                price_pyeong = round(price_pyeong, 2)
            except ValueError:
                string_value = price.split('/')[-1].replace(',','').split(" ")
                float_value = float(string_value[0].replace('억', '00000000')) + float(string_value[1])
                price_pyeong = round(float_value/float(contract_space), 2)
        if space_type == '대지/연 면적':
            row = [num, category, title, date, floor, feature, trade_type, price, price_pyeong, np.nan, np.nan, contract_space, whole_space, url]
            row_df = pd.DataFrame([row], columns=['매물 번호','매물유형', '매물명', '날짜', '층', '매물 특징','거래방식', '가격', '평당금액(만원)', '계약 면적(평)', '전용 면적(평)', '대지 면적(평)', '연 면적(평)', '링크'])
        else:
            row = [num, category, title, date, floor, feature, trade_type, price, price_pyeong, contract_space, whole_space, np.nan, np.nan, url]
            row_df = pd.DataFrame([row], columns=['매물 번호','매물유형', '매물명', '날짜', '층', '매물 특징','거래방식', '가격', '평당금액(만원)', '계약 면적(평)', '전용 면적(평)', '대지 면적(평)', '연 면적(평)', '링크'])
        df = df.append(row_df, ignore_index=True)
        df.to_csv(f'{query}.csv', encoding='utf-8')
    browser.close()
    clean_data(query)