import requests
from bs4 import BeautifulSoup
import pandas as pd

user_agent = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

title_class = "_sp_each_title"
company_class = "_sp_each_source"
summary_text = 'ul.type01 dl'


TITLE = []
COMPANY = []
SUMMARY = []
HREF = []


def query_naver(q: str, p: int, enable_recent: bool):
    if enable_recent == False:
        r =requests.get(f'https://search.naver.com/search.naver?&where=news&query={q}&sort=0&start={p*10}', headers=user_agent)
        soup = BeautifulSoup(r.text, 'html.parser')
    else: 
        r =requests.get(f'https://search.naver.com/search.naver?&where=news&query={q}&sort=1&start={p*10}', headers=user_agent)
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_function(soup):
    s = soup.find_all("a", {"class": f"{title_class}"})
    for t in s:
        TITLE.append(t['title'])
        HREF.append(t['href'])

    s = soup.find_all('span', {'class': f'{company_class}'})
    for t in s:
        COMPANY.append(t.text)

    dl = soup.select(summary_text)
    for d in dl:
        ddl = d.select('dd')
        SUMMARY.append(ddl[1].text)
    return  

def search_naver(num, query, enable_recent=False):
    if enable_recent == False:
        for i in range(0, num):
            soup = query_naver(query, i, enable_recent=False)
            get_function(soup)
    else: 
        for i in range(0, num):
            soup = query_naver(query, i, enable_recent=True)
            get_function(soup)
    data = {
        '제목': TITLE,
        '보도사': COMPANY,
        '요약': SUMMARY,
        '링크': HREF
    }
    df = pd.DataFrame(data)
    df.to_csv(f"{query}.csv")
    return df

with open('request.txt', 'r', encoding='utf-8') as f:
    request_list = f.readlines()
    item_list = [request.replace("\n", "") for request in request_list]
print(f'---------------------------------------\n\n요청 아이템 수: {len(item_list)}\n\n---------------------------------------\n\n')
for r in request_list:
    search_naver(50, r)