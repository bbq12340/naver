# -*- coding: utf-8 -*- 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import messagebox
import functools

from pagination import get_pages
from browser import open_browser,get_browser
from extract_naver_map import enter_frame
from clean_data import clean_data

root = tk.Tk()
root.title('네이버 지도 크롤러')
root.geometry("200x150")

#var
loc = tk.StringVar()
keyword = tk.StringVar()


def extract_naver_map():
    query = loc.get()+" "+keyword.get()
    browser = open_browser(query)
    wait = WebDriverWait(browser, 30)
    by_id = By.ID, 'searchIframe'
    wait.until(EC.presence_of_element_located(by_id))
    last_page = int(get_pages(browser))
    get_browser(browser, query)
    wait.until(EC.presence_of_element_located(by_id))
    browser.switch_to.frame('searchIframe')
    for p in range(last_page):
        print(f"extracting page{p+1}/{last_page}")
        time.sleep(1)
        #first 10 items
        atags = browser.find_elements_by_class_name('_2aE-_')
        atags[-1].click()
        #browse through list
        n = 1
        while True:
            n = n+1
            if n == len(atags):
                break
            atags[n].click()
            atags = browser.find_elements_by_class_name('_2aE-_')
        #extract
        atags = browser.find_elements_by_class_name('_2aE-_')
        for a in atags:
            a.click()
            enter_frame(browser, wait, query)
        #click next page
        next_btn = browser.find_elements_by_class_name('_3pA6R')[1]
        next_btn.click()
    print('finished!')
    clean_data(query)
    messagebox.showinfo('info', '완료')

#label
loc_label = tk.Label(root, text="지역")
loc_label.grid(row=0, column=0)

keyword_label = tk.Label(root, text="키워드")
keyword_label.grid(row=1, column=0)

#entry
loc_entry = tk.Entry(root, width=10, textvariable=loc)
loc_entry.grid(row=0, column=1)

keyword_entry = tk.Entry(root, width=10, textvariable=keyword)
keyword_entry.grid(row=1, column=1)


#button
search_btn = tk.Button(root, text='검색', height=1, width=7, command=extract_naver_map)
search_btn.grid(row=2, column=1, pady=5, columnspan=2)

root.mainloop()