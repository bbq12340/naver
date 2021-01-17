import requests, re
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs


class Scraper():
    def __init__(self, delay):
        self.API_URL = "https://news.naver.com/main/list.nhn"
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        }
        self.delay = delay
        
    def extract_naver_news_article(self, link):
        NAVER_NEWS_URL = link
        r = requests.get(NAVER_NEWS_URL, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        with open("soup.txt", "w") as f:
            f.write(r.text)
        article_date = soup.find_all('span', {'class': 't11'})[-1].text
        article_body = soup.find('div', {'class': '_article_body_contents'}).text
        article_body = re.sub('[\n\t\r]', ' ', article_body)
        data = {
            "article_date": article_date,
            "article_body": article_body
        }
        return data
    
    def extract_naver_news_main(self, query, dateFrom, dateTo, amount=float('inf')):
        NAVER_URL = "https://search.naver.com/search.naver"
        start = 1
        count = 0
        payload = {
            "where": "news",
            "query": query,
            "sort": 0,
            "ds": dateFrom,
            "de": dateTo,
            "start": start
        }
        while True:
            data = {
                "dates": [], # 날짜
                "titles": [], # 제목
                "summaries": [], # 요약
                "articles": [], # 본문
                "links": [] # 링크
            }
            r = requests.get(NAVER_URL, params=payload, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            ul = soup.find("ul",{"class":"list_news"}).find_all("li", {"class":"bx"})
            for li in ul:
                try:
                    data['links'].append(li.find('div', {'class':'news_area'}).find('a',string="네이버뉴스")['href'])
                    data['titles'].append(li.find('a',{'class':'news_tit'})['title'])
                    data['summaries'].append(li.find('a',{'class':'dsc_txt_wrap'}).text)
                    count += 1
                except:
                    pass
            for link in data['links']:
                article = self.extract_naver_news_article(link)
                data['dates'].append(article['article_date'])
                data['articles'].append(article['article_body'])
                time.sleep(self.delay)
            payload["start"] += 10
            df = pd.DataFrame(data, columns=list(data.keys()))
            df.to_csv(f'result/{query}.csv', encoding='utf-8-sig', mode='a', header=False, index=False)
            if len(ul) < 10:
                self.finished.emit()
                return
            if count >= amount:
                break
    
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
        self.email_format = re.compile(r"[0-9a-zA-Z\.-]+@[0-9a-zA-Z\.-]+\.[a-zA-Z\.]+")
        self.reporter_format = re.compile(r'[가-힣]{2,3}\s?기자[\n\s\t]')
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


        
