import requests
from bs4 import BeautifulSoup

class MallScraper:
    def __init__(self, root, progress, progress_label):
        self.root = root
        self.progress = progress
        self.progress_label = progress_label
        self.URL = "https://search.shopping.naver.com/mall/list.nhn"
        self.headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "referer": "https://search.shopping.naver.com/mall/mall.nhn"
        }
        with open("list.txt", "w") as f:
            f.write("")
        return
    def query(self, category, word, sort, sp, ep, key):
        LINKS = []
        for p in range(sp, ep+1):
            self.progress_label.config(text=f"{p}페이지 수집중...")
            payload = {
            "category": category,
            "prefix": word,
            "sortingOrder": sort,
            "page": p,
            "pagesize": "20",
            "name":key
            }
            r = requests.get(self.URL, headers=self.headers, params=payload)
            soup = BeautifulSoup(r.text, 'html.parser')
            urls = soup.find_all('td',{'class':'url'})
            for u in urls:
                u = u.find('a')
                if "smartstore.naver.com" in u.text:
                    LINKS.append("https://"+u.text)
        for l in LINKS:
            with open("list.txt", "a") as f:
                f.write("https://"+l+"\n")
        return LINKS

        
