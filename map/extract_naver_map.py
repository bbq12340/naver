from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def enter_frame(browser, wait, query):
    by_a = By.CLASS_NAME, '_1S2_U'
    by_id = By.ID, 'entryIframe'
    by_id_frame = By.ID, 'searchIframe'
    browser.switch_to_default_content()
    wait.until(EC.presence_of_element_located(by_id))
    browser.switch_to.frame('entryIframe')
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(by_a))
    html = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('span', {'class': '_3XamX'}).text
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
    wait.until(EC.presence_of_element_located(by_id_frame))
    browser.switch_to.frame('searchIframe')
    return browser


        