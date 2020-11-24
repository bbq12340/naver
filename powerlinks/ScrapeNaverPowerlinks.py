from typing import Type
import requests, re, json
from bs4 import BeautifulSoup
import pandas as pd

class Scraper():
    def __init__(self, query, progress, master):
        self.query = query
        self.progress = progress
        self.master = master
        self.API_URL = "https://ad.search.naver.com/search.naver"
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        }
        self.PHONE_FORM = re.compile(r'(\d{2,3})\D+(\d{3,4})-(\d{4})')
        
        return
    
    def extract_powerlinks(self):
        extracted = []
        p=1
        self.progress['value'] = 10
        self.master.update_idletasks()
        while True:
            params = {
            "where": "ad",
            "query": self.query,
            "pagingIndex": p,
            "bucket": "0"
            }
            r = requests.get(self.API_URL, params=params, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find('div',{"class":"sp_notfound"}):
                self.progress['value'] = 90
                self.master.update_idletasks()
                break
            lists = soup.find_all('li', {'class': 'lst'})
            for l in lists:
                data = {
                    '제목': l.find('div', {'class': 'inner'}).find('a').text.replace("\n",""),
                    '내용': re.sub(' +', ' ',l.find('div', {'class': 'ad_dsc'}).text.replace("\n","")),
                    'url': l.find('div', {'class': 'inner'}).find('div',{'class':'url_area'}).find('a').text
                }
                extracted.append(data)
            p = p+1
            self.progress['value'] += 5
            self.master.update_idletasks()
        df = pd.DataFrame(extracted)
        self.progress['value'] = 100
        self.master.update_idletasks()
        return df
    
    def extract_phone(self):
        index_names = []
        phones = []
        df = self.extract_powerlinks()
        for url in df['url']:
            if "blog.naver.com/" in url:
                id = url.split('/')[-1]
                business_url = "https://m.blog.naver.com/rego/BusinessInfo.nhn"
                introduction_url = "https://m.blog.naver.com/rego/Introduce.nhn"
                headers = {
                    'referer': url,
                    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
                }
                params = {
                    "blogId": id
                }
                r = requests.get(business_url, params=params, headers=headers)
                data = json.loads(r.text.split('\n')[1])
                try:
                    phone = data['result']['businessView']['phone']
                except TypeError:
                    r = requests.post(introduction_url, data=params, headers=headers)
                    data = json.loads(r.text.split('\n')[1])
                    try:
                        phone = data['result']['phoneNumber']
                    except TypeError:
                        phone = None
                phones.append(phone)

            elif "http://cafe.naver.com/" in url:
                r = requests.get(url, headers=self.headers)
                phone = self.PHONE_FORM.search(r.text).group(0)
                phones.append(phone)
            else:
                index_names.append(list(df['url']).index(url))
                phone = None

        df.drop(index_names, inplace=True)
        df['전화번호'] = phones
        print(df.head)
        return df
