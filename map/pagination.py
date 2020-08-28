import time
def get_pages(browser):
    time.sleep(3)
    browser.switch_to.frame('searchIframe')
    while True:
        current_page = browser.find_element_by_class_name('gK3dR')
        pages = browser.find_elements_by_class_name('zJJPW')
        pages[-1].click()
        if current_page == pages[-1]:
            break
    return current_page.get_attribute('innerText')

