from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def open_browser(query):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(f'https://map.naver.com/v5/search/{query}')
    return browser
def get_browser(browser, query):
    browser.get(f'https://map.naver.com/v5/search/{query}')
    print(f'searching {query}...')
    return browser