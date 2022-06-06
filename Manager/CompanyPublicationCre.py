import sys
import time

from selenium.common.exceptions import NoSuchElementException #导入一个没有这个元素的类，定位到没有这个元素会抛出一个异常
from Config.SeleniumConfig import clear_window_tabs, initial_chrome_driver, switch_window_tab
from Config.pyConfig import set_user_sleep_time
from Creeper.AdvanceQuery import cnki_advance_search, author_advance_search
from Parser.ResultListParse import result_items_parse, open_result_item_detail, parse_authority_name, \
    parse_publisher_type, open_publisher_info_page, parse_publisher_complex_factor, parse_publish_year



input_file_url = r"D:\BaiduNetdiskDownload\intotal_no22_1.txt"
output_file_url = r"D:\BaiduNetdiskDownload\outtotal_no22_1.txt"


class FakeElement:
    def __init__(self):
        self.text = ""


def a_company_info(browser, query: str, info_file_url=None):

    output = []

    browser = cnki_advance_search(browser)
    time.sleep(set_user_sleep_time())
    browser = author_advance_search(browser, query)
    result_handle_page = browser.current_window_handle
    # print(result_handle_page)
    # print(browser.window_handles)
    cur_ind = -1

    while(True):

        time.sleep(set_user_sleep_time())
        item_list = result_items_parse(browser)
        for ind in range(len(item_list)):
            try:

                # print("-----stage  --  1  -----")
                item_list = result_items_parse(browser)
                if ind <= cur_ind:
                    continue
                cur_ind += 1
                if cur_ind == len(item_list):
                    break
                item = item_list[cur_ind]

                # print("-----stage  --  2  -----")
                # //*[@id="gridTable"]/table/tbody/tr[1]/td[6]
                if item.find_element_by_class_name('data').text != "期刊":
                    continue
                time.sleep(set_user_sleep_time())

                try:
                    ds_date = parse_publish_year(item)
                except Exception as e:
                    ds_date = ""

                try:
                    date = ds_date.split("-")
                except Exception as e:
                    date = []

                try:
                    aricle_name = item.find_element_by_class_name('name').text
                except Exception as e:
                    aricle_name = ""

                # print("-----stage  --  3  -----")
                browser = open_result_item_detail(browser, item)

                time.sleep(set_user_sleep_time())
                authorities = parse_authority_name(browser)
                types = parse_publisher_type(browser)

                time.sleep(set_user_sleep_time())

                # print("-----stage  --  4  -----")
                try:
                    browser, publisher_name = open_publisher_info_page(browser)
                    factor, now_type = parse_publisher_complex_factor(browser)

                except NoSuchElementException as e:
                    factor = ""
                    publisher_name = ""
                    now_type = ""
                    print("期刊没有影响因子 或 非学术期刊：\n {}".format("NoSuchElementException"))

                # print("-----stage  --  5  -----")
                output_str = "{},{},{},{},{},{},{},{}".format(query, aricle_name, ",".join(date), "\t".join(authorities),
                                                           "\t".join(types), factor, publisher_name, "\t".join(now_type))
                # output.append(output_str)
                with open(info_file_url, "a", encoding='utf-8') as output_file:
                    output_file.write("{}\n".format(output_str))
                    output_file.flush()
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), end="\t: ")
                print(output_str)
            finally:
                # print("-----stage  --  6  -----")
                # print(result_handle_page)
                # print(browser.window_handles)
                time.sleep(set_user_sleep_time())
                # sys.stdout.write("begin to clear windows\n")
                # print("start cleaning browser")
                browser = clear_window_tabs(browser, result_handle_page)
                time.sleep(10)
                # print("finish cleaning")

        # /html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[2]/a[11]
        # //*[@id="PageNext"]
        pages_list = browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[2]/a')

        if len(pages_list) == 0:
            break
        if pages_list[-1].text != "下一页":
            break
        else:
            cur_ind = -1
            pages_list[-1].click()
            result_handle_page = browser.current_window_handle

    return
    # "\n".join(output)


def all_company_info_io(company_file_url: "str", info_file_url: "str"):
    browser = initial_chrome_driver(visualize=True, img_enable=True)  # )
    with open(company_file_url, "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            try:
                a_company_info(browser, line.strip(), info_file_url)
                # with open(info_file_url, "a", encoding='utf-8') as output_file:
                #     output_file.write("{}\n".format(company_info))
                #     output_file.flush()
            except Exception as e:
                print(e)
    browser.quit()


if __name__ == '__main__':

     # all_company_info_io(input_file_url, output_file_url)
    sys.path.append(r"C:\\Users\\DELL\\Desktop\\CNKIPublishCreeper\\Config")
    # sys.path.append(r"C:\Users\DELL\Desktop\CNKIPublishCreeper\Creeper\\")
    # sys.path.append(r"C:\Users\DELL\Desktop\CNKIPublishCreeper\Manager\\")
    #  sys.path.append(r"C:\Users\DELL\Desktop\CNKIPublishCreeper\\")
    browser = initial_chrome_driver()
    company_info = a_company_info(browser, "广州港股份有限公司")
    print(company_info)
    browser.close()
