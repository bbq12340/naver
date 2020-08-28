
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def open_estate(query):
    NAVER_ESTATE = 'https://land.naver.com/'
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(NAVER_ESTATE)
    query_input = browser.find_element_by_id('queryInputHeader')
    query_input.send_keys(query)
    time.sleep(1)
    query_input.send_keys(Keys.RETURN)
    APT_URL = browser.current_url
    TARGET_URL = APT_URL.replace('complexes', 'offices').replace('APT', 'SG:SMS:GJCG:APTHGJ:GM:TJ')
    browser.get(TARGET_URL)
    return browser