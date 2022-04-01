################################################
import sys
import time

from Config.SeleniumConfig import initial_chrome_driver, switch_window_tab

################################################

def cnki_advance_search(browser):

    browser.get("https://www.cnki.net/")

    adv_search = browser.find_element_by_xpath('//*[@id="highSearch"]')
    adv_search.click()
    browser = switch_window_tab(browser)

    return browser


def author_advance_search(browser, author: str):

    browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/ul/li[3]').click()

    author_box = browser.find_element_by_xpath('//*[@id="autxt"]/dd[2]/div[2]/input')
    author_box.clear()
    author_box.send_keys(author)

    search_button = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input')
    search_button.click()

    return browser


if __name__ == '__main__':
    driver = initial_chrome_driver()
    driver.get("https://www.cnki.net/")
    time.sleep(5)
    driver.close()
    print(sys.path)
