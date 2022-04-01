
################################################
import sys
import os
import time

from selenium import webdriver

################################################


pwd = os.path.split(os.path.realpath(__file__))
print("\nPrint Work Directory: Config Dir: \n {}".format(pwd[0]))
chromedriver_path = os.path.join(pwd[0], "chromedriver.exe")
if chromedriver_path not in sys.path:
    sys.path.append(os.path.join(pwd[0], "chromedriver.exe"))
    print("Chrome Driver Exe is ADDED in Path AS: \n {} \n".format(sys.path[-1]))
else:
    print("Chrome Driver Exe is already ADDED in Path: \n {} \n".format(chromedriver_path))


def initial_chrome_driver(visualize: bool = False, scrollbar: bool = False,
                          img_enable: bool = False, implicitly_wait: tuple = (True, 5)):

    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug

    if visualize:
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    if scrollbar:
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    if img_enable:
        chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

    browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    if implicitly_wait[0]:
        browser.implicitly_wait(implicitly_wait[1])  # implicitly_wait等待5秒，最多等待5s，超过5秒就会报错
    return browser


def switch_window_tab(browser, windows_list: list = None, to_page=-1):

    handle = browser.current_window_handle
    if windows_list is None:
        windows_list = browser.window_handles

    if isinstance(to_page, int):
        if handle != windows_list[to_page]:
            browser.switch_to.window(windows_list[to_page])
    elif isinstance(to_page, str) &\
            (handle != to_page) & (to_page in windows_list):
        browser.switch_to.window(to_page)

    return browser


def clear_window_tabs(browser, save_page=0):

    windows_list = browser.window_handles
    if len(windows_list) == 1:
        return browser

    for i in range(len(windows_list)):
        if (save_page == i) | (save_page == windows_list[i]):
            continue
        browser.switch_to.window(windows_list[i])
        browser.close()
    browser.switch_to.window(browser.window_handles[0])

    return browser


if __name__ == '__main__':
    driver = initial_chrome_driver()
    driver.get("https://www.baidu.com/")
    time.sleep(5)
    driver.close()
