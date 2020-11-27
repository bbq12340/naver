
import requests, re
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, date):
        self.API_URL  = "https://news.naver.com/main/list.nhn"
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        }
        self.date = date
        self.email_format = re.compile(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    
    def extract_main_url(self, page):
        extracted_mails = []
        params = {
            "mode": "LSD",
            "mid": "sec",
            "sid1": "105",
            "date": self.date,
            "page": page
        }
        r = requests.get(self.API_URL, params=params, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.paser')
        headlines = soup.find('ul', {'class':'type06_headline'}).find_all('li')
        for head in headlines:
            url = head.find('a')['href']
            mail = self.extract_reporter(url)
            extracted_mails.append(mail)
        return

    def extract_reporter(self, url):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.pasrser')
        
        email = self.email_format.search(soup.find('div',{'class':'_article_body_contents'}).text).group(0)
        return email
