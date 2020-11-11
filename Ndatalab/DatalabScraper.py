from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import trange
import time

KEYWORD_XPATH = By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[1]/a'
NXT_BTN_XPATH = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]'

class Scraper():
    def __init__(self, code):
        self.code = code
        self.options = self.headless_browser()
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.wait = WebDriverWait(self.browser, 30)

    def headless_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        return options

    def scrape_document(self):
        KEYWORDS = []
        self.browser.get(f'https://datalab.naver.com/shoppingInsight/sCategory.naver?cid={self.code}')
        self.wait.until(EC.presence_of_element_located(KEYWORD_XPATH))
        for p in trange(0,25):
            html = self.browser.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, 'html.parser')
            page_keywords = self.scrape_keywords(soup)
            KEYWORDS.extend(page_keywords)
            #click next page
            nxt_btn = self.browser.find_element_by_xpath(NXT_BTN_XPATH)
            nxt_btn.click()
            time.sleep(1)
        return KEYWORDS
    def scrape_keywords(self, soup):
        keyword_list = soup.find('ul',{'class':'rank_top1000_list'}).find_all('li')
        result = []
        for word in keyword_list:
            ranking = word.find('span', {'class':'rank_top1000_num'}).text
            data = {
                '키워드': word.text.replace('\n','').replace(' ','').replace(ranking,''),
                '링크': "https://datalab.naver.com"+word.find('a')['href']
            }
            result.append(data)
        return result
