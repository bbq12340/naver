import requests
from bs4 import BeautifulSoup
import pandas as pd

def nblog_crawler(query, max_pages):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    df = pd.DataFrame([],columns=['날짜', '출처', '제목', '내용', 'URL'])
    for page in range(max_pages):
        r = requests.get(f"https://search.naver.com/search.naver?where=post&sm=tab_jum&query={query}&start={1+(page*10)}", headers=user_agent)
        soup = BeautifulSoup(r.text, 'html.parser')
        blog_list = soup.find_all('li', {'class': 'sh_blog_top'})
        for blog in blog_list:
            row = [
                blog.find('dd',{'class':'txt_inline'}).text, '네이버 블로그', blog.find('a',{'class':'sh_blog_title'})['title'], blog.find('dd',{'class':'sh_blog_passage'}).text, blog.find('a', {'class':'sh_blog_title'})['href']
            ]
            row_df = pd.DataFrame([row], columns=['날짜', '출처', '제목', '내용', 'URL'])
            df = df.append(row_df, ignore_index=True)
    df.set_index('날짜', inplace=True)
    df.to_csv('data.csv', encoding='utf-8')