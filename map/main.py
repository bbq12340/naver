# -*- coding: utf-8 -*- 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time, csv
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup

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
    by_xpath = By.XPATH, "//object[@id='searchIframe']"
    wait.until(EC.presence_of_element_located(by_xpath))
    time.sleep(3)
    search_frame = browser.find_element_by_xpath("//object[@id='searchIframe']")
    browser.switch_to.frame(search_frame)
    last_page = int(get_pages(browser))
    get_browser(browser, query)
    wait.until(EC.presence_of_element_located(by_xpath))
    search_frame = browser.find_element_by_xpath("//object[@id='searchIframe']")
    browser.switch_to.frame(search_frame)
    for p in range(last_page):
        print(f"extracting page{p+1}/{last_page}")
        time.sleep(1)
        while True:
            atags_1 = browser.find_elements_by_class_name('_2aE-_')
            browser.execute_script("document.querySelector('._1Az1K').scrollTo(document.querySelector('._1Az1K').scrollTop, document.querySelector('._1Az1K').scrollHeight);")
            atags = browser.find_elements_by_class_name('_2aE-_')
            if len(atags_1) == len(atags):
                break
        #extract
        by_xpath = By.XPATH, '//object[@id="entryIframe"]'
        for a in atags:
            a.click()
            print(atags.index(a)+1)
            #wait.until(EC.presence_of_element_located(by_xpath))
            #url = browser.find_elements_by_tag_name('object')[1].get_attribute('data')
            #body = browser.find_element_by_tag_name("body")
            #body.send_keys(Keys.CONTROL + 't')
            #body.get(url)
            #browser.switch_to_window(browser.window_handles[-1])
            html = browser.execute_script("return document.documentElement.outerHTML")
            with open('new_html.txt', 'w') as f:
                f.write(html)
            soup = BeautifulSoup(html,'html.parser')
            title = soup.find('span', {'class': '_3XamX'}).text
            address = soup.find('span',{'class': '_2yqUQ'}).text
            phone = soup.find('li', {'class': '_3xPmJ'})
            if phone:
                phone = phone.text.split('안내')[0]
            else:
                phone = None
            browser.close()
            browser.switch_to_window(browser.window_handles[0])
            with open(f'{query}.csv', 'a', encoding='utf-8') as csvfile:
                csvfile_writer = csv.writer(csvfile, delimiter=',')
                csvfile_writer.writerow([title, address, phone])
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