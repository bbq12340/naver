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
import tkinter as tk
from tkinter import messagebox


PACK = By.CLASS_NAME, "main_pack"


def open_browser(query, num, datetype, facetype):
#    options = Options()
#    options.add_argument('--headless')
#    options.add_argument('--disable-gpu')  
    NAVER = f"https://search.naver.com/search.naver?where=image&section=image&query={query}&datetype={datetype}&face={facetype}"
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(NAVER)
    imgs = browser.find_elements_by_class_name("_img")
    wait = WebDriverWait(browser, 10)
    

    while len(imgs) < num:
        last_length = len(imgs)
        time.sleep(1)
        max_height = "document.body.scrollHeight"
        browser.execute_script(f"window.scrollBy(0, {max_height});")
        wait.until(EC.presence_of_element_located(PACK))
        time.sleep(1)
        imgs = browser.find_elements_by_class_name("_img")
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
                break
            except Exception:
                with open("error.txt", 'a') as f:
                    f.write(f"{imgs.index(img)}--invalid")
    messagebox.showinfo("info", "작업완료.")
    return

root = tk.Tk()
root.title('네이버 이미지 크롤러')
root.geometry("300x150")

#function
def extract_image():
    if datetype.get() == 1 and facetype.get() == 1:
        imgs = open_browser(keyword.get(), limit.get(), datetype=5, facetype=1)
        get_imgs(imgs, keyword.get())
    elif datetype.get() == 1 and facetype.get() == 0:
        imgs = open_browser(keyword.get(), limit.get(), datetype=5, facetype=0)
        get_imgs(imgs, keyword.get())
    elif datetype.get() == 0 and facetype.get() == 1:
        imgs = open_browser(keyword.get(), limit.get(), datetype=0, facetype=1)
        get_imgs(imgs, keyword.get())
    else:
        imgs = open_browser(keyword.get(), limit.get(), datetype=0, facetype=0)
        get_imgs(imgs, keyword.get())
#var
keyword = tk.StringVar()
limit = tk.IntVar()
datetype = tk.IntVar()
facetype = tk.IntVar()

#label
keyword_label = tk.Label(root,text="키워드")
keyword_label.grid(row=0, column=0, padx=5, pady=5)

limit_label = tk.Label(root, text="갯수")
limit_label.grid(row=1, column =0, padx=5, pady=5)

#entry
keyword_entry = tk.Entry(root, textvariable=keyword)
keyword_entry.grid(row=0, column=1)

limit_entry = tk.Entry(root, textvariable=limit)
limit_entry.grid(row=1, column=1)

#checkbox
date_box = tk.Checkbutton(root, text="1년", variable=datetype)
date_box.grid(row=2, column=0)

face_box = tk.Checkbutton(root, text="인물중심", variable=facetype)
face_box.grid(row=2, column=1)

#button
search_btn = tk.Button(root, text="검색", command=extract_image)
search_btn.grid(row=3, column=1, columnspan=2, pady=5)

root.mainloop()