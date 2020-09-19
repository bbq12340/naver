from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://map.naver.com/v5/search/%EA%B0%95%EB%82%A8%20%ED%9C%B4%EB%8C%80%ED%8F%B0/place/36893224?c=14138963.1936218,4509822.8873395,13,0,0,0,dh&placePath=%3F%2526')
entry_frame = browser.find_element_by_xpath("//object[@id='entryIframe']")
browser.switch_to.frame(entry_frame)
html = browser.execute_script('return document.body.outerHTML')
with open ('entryframe.txt', 'w') as f:
    f.write(html)
browser.quit()