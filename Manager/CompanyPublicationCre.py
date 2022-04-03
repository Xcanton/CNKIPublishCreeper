import sys
import time

from selenium.common.exceptions import NoSuchElementException #导入一个没有这个元素的类，定位到没有这个元素会抛出一个异常
from Config.SeleniumConfig import clear_window_tabs, initial_chrome_driver, switch_window_tab
from Config.pyConfig import set_user_sleep_time
from Creeper.AdvanceQuery import cnki_advance_search, author_advance_search
from Parser.ResultListParse import result_items_parse, open_result_item_detail, parse_authority_name, \
    parse_publisher_type, open_publisher_info_page, parse_publisher_complex_factor, parse_publish_year


class FakeElement:
    def __init__(self):
        self.text = ""


def a_company_info(browser, query: str):

    output = []

    browser = cnki_advance_search(browser)
    time.sleep(set_user_sleep_time())
    browser = author_advance_search(browser, query)
    result_handle_page = browser.current_window_handle

    while(True):

        time.sleep(set_user_sleep_time())
        for item in result_items_parse(browser):

            time.sleep(set_user_sleep_time())
            ds_date = parse_publish_year(item)
            date = ds_date.split("-")
            browser = open_result_item_detail(browser, item)

            time.sleep(set_user_sleep_time())
            authorities = parse_authority_name(browser)
            types = parse_publisher_type(browser)

            time.sleep(set_user_sleep_time())
            try:
                browser, publisher_name = open_publisher_info_page(browser)
                factor = parse_publisher_complex_factor(browser)
            except NoSuchElementException as e:
                factor = ""
                publisher_name = ""
                print("期刊没有影响因子 或 非学术期刊：\n {}".format("NoSuchElementException"))

            output_str = "{},{},{},{},{},{}".format(query, ",".join(date), "\t".join(authorities),
                                                    "\t".join(types), factor, publisher_name)
            output.append(output_str)
            print(output_str)
            time.sleep(set_user_sleep_time())
            # sys.stdout.write("begin to clear windows\n")
            browser = clear_window_tabs(browser, result_handle_page)

        # //*[@id="page3"]
        pages_list = browser.find_elements_by_xpath('//*[@id="PageNext"]')

        if len(pages_list) == 0:
            break
        if pages_list[-1].text != "下一页":
            break
        else:
            pages_list[-1].click()
            result_handle_page = browser.current_window_handle

    return "\n".join(output)


def all_company_info_io(company_file_url: str, info_file_url: str):
    browser = initial_chrome_driver(visualize=True, img_enable=True)
    with open(company_file_url, "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            try:
                company_info = a_company_info(browser, line.strip())
                with open(info_file_url, "a", encoding='utf-8') as output_file:
                    output_file.write("{}\n".format(company_info))
                    output_file.flush()
            except:
                pass
    browser.quit()


if __name__ == '__main__':
    input_file_url = r"D:\BaiduNetdiskDownload\input.txt"
    output_file_url = r"D:\BaiduNetdiskDownload\output.txt"
    all_company_info_io(input_file_url, output_file_url)
