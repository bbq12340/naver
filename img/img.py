from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import urllib
import os
import time
from tkinter import messagebox


PACK = By.CLASS_NAME, "main_pack"


def open_browser(query, num, datetype, facetype):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  
    NAVER = f"https://search.naver.com/search.naver?where=image&section=image&query={query}&datetype={datetype}&face={facetype}"
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(NAVER)
    imgs = browser.find_elements_by_class_name("_img")
    wait = WebDriverWait(browser, 10)
    

    while len(imgs) < num:
        last_length = len(imgs)
        print(last_length)
        time.sleep(1)
        max_height = "document.body.scrollHeight"
        browser.execute_script(f"window.scrollBy(0, {max_height});")
        wait.until(EC.presence_of_element_located(PACK))
        time.sleep(1)
        imgs = browser.find_elements_by_class_name("_img")
        print(len(imgs))
        if len(imgs) == last_length:
            messagebox.showerror("에러", "요청수가 아이템 수를 초과했습니다.")
            browser.close()
            break
        if len(imgs) >= num:
            html = browser.execute_script("return document.body.outerHTML;")
            browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            imgs = soup.select("._img")
            imgs = imgs[:num]
            break
    return imgs

def get_imgs(imgs, query):

    os.mkdir(f"{query}")

    for img in imgs:

        while True:
            try:
                urllib.request.urlretrieve(img['src'], f"{query}/{imgs.index(img)}.jpg")
            except Exception:
                with open("error.txt", 'a') as f:
                    f.write(f"{imgs.index(img)}--invalid")
                continue
            break
    return