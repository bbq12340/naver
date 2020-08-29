from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def enter_frame(browser, wait, query):
    #by_ul = By.CLASS_NAME, "_6aUG7"
    by_xpath = By.XPATH, "//object[@id='entryIframe']"
    browser.switch_to_default_content()
    wait.until(EC.presence_of_element_located(by_xpath))
    entry_frame = browser.find_element_by_xpath("//object[@id='entryIframe']")
    browser.switch_to.frame(entry_frame)
    html = browser.execute_script("return document.documentElement.outerHTML")
    with open('new_html.txt' ,'a')as f:
        f.write(html+"\n")
    time.sleep(1)
    #wait.until(EC.presence_of_element_located(by_ul))
    html = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('span', {'class': '_3XamX'}).text
    print(title)
    address = soup.find('span',{'class': '_2yqUQ'}).text
    phone = soup.find('li', {'class': '_3xPmJ'})
    if phone:
        phone = phone.text.split('안내')[0]
    else:
        phone = None
    with open(f'{query}.csv', 'a', encoding='utf-8') as csvfile:
        csvfile_writer = csv.writer(csvfile, delimiter=',')
        csvfile_writer.writerow([title, address, phone])
    browser.switch_to_default_content()
    search_frame = browser.find_element_by_xpath("//object[@id='searchIframe']")
    browser.switch_to.frame(search_frame)
    return browser


        