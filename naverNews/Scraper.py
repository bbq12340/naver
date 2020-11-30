import requests, re
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs


class Scraper():
    def __init__(self):
        self.API_URL = "https://news.naver.com/main/list.nhn"
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        }
        self.email_format = re.compile(r"[0-9a-zA-Z\.-]+@[0-9a-zA-Z\.-]+\.[a-zA-Z\.]+")
        self.reporter_format = re.compile(r'[가-힣]{2,3}\s?기자[\n\s\t]')
    
    def extract_main_url(self, url, page):
        extracted = []
        parsed = parse_qs(urlparse.urlparse(url).query)
        params = {
            "mode": parsed['mode'][0],
            "mid": parsed['mid'][0],
            "sid1": parsed['sid1'][0],
            "page": page
        }
        r = requests.get(self.API_URL, params=params, headers=self.headers)
        if r.status_code != 200:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        headlines1 = soup.find('ul', {'class':'type06_headline'}).find_all('li')
        for head in headlines1:
            url = head.find('a')['href']
            data = self.extract_reporter(url)
            extracted.append(data)
        headlines2 = soup.find('ul',{'class':'type06'}).find_all('li')
        for head in headlines2:
            url = head.find('a')['href']
            data = self.extract_reporter(url)
            extracted.append(data)
        return extracted

    def extract_reporter(self, url):
        print(url)
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        article_body = soup.find('div',{'class':'_article_body_contents'})
        try:
            email = self.email_format.findall(article_body.text)[-1]
        except:
            email = None
        try:
            reporter = self.reporter_format.findall(article_body.text)[-1].replace('기자','')
        except:
            reporter = None
        data = {
            'reporter': reporter,
            'email': email,
            'link': url
        }
        return data


        
