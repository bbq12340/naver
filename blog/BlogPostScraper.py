import requests
from bs4 import BeautifulSoup
import json

class Scraper:
    def __init__(self, username):
        self.username = username
        self.API_url = 'https://m.blog.naver.com/rego/PostListInfo.nhn'
        self.header = {
            'authority': 'm.blog.naver.com',
            'method': 'GET',
            'scheme': 'https',
            'referer': 'https://m.blog.naver.com/susie9211',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }

    def get_blog_info(self):
        url = 'https://m.blog.naver.com/rego/CategoryList.nhn'
        payload = {
            'blogId': self.username
        }
        r = requests.get(url, params=payload, headers=self.header)
        json_data = json.loads(r.text.split('\n')[1])
        total_posts = json_data['result']['mylogPostCount']
        print(f"총 포스트: {total_posts}")
        return total_posts

    def get_post_info(self, page):
        scraped_posts = []
        payload = {
            'blogId': self.username,
            'categoryNo': 0,
            'currentPage': page,
            'logCode': 0
        }
        r = requests.get(self.API_url, params=payload, headers=self.header)
        json_data = json.loads(r.text.split('\n')[1])
        view_list = json_data['result']['postViewList']
        for post in view_list:
            scraped_posts.append(post['logNo'])
        return scraped_posts
