import requests, urllib, wget, time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://search.shopping.naver.com/search/all?query=%EC%86%90%EB%8B%98%EB%B0%A9%EB%AC%B8%EC%95%8C%EB%A6%BC%20%EB%8F%84%EC%96%B4%EB%B2%A8(SN-2201)%EC%8B%A0%ED%98%B8%EA%B8%B0%20%EB%8F%84%EC%96%B4%EB%B2%A8%20%22%EC%86%90%EB%8B%98%EB%B0%A9%EB%AC%B8%EC%95%8C%EB%A6%BC%20%EB%8F%84%EC%96%B4%EB%B2%A8(SN-2201)%EC%8B%A0%ED%98%B8%EA%B8%B0%20%EB%8F%84%EC%96%B4%EB%B2%A8%22&sort=review')
time.sleep(1)
xpath = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[1]/li/div/div[1]/div/a/img')
print(xpath)