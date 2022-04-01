################################################


from Config.SeleniumConfig import switch_window_tab
################################################


def result_items_parse(browser):
    items_box = browser.find_elements_by_xpath('//*[@id="gridTable"]/table/tbody/tr')
    return items_box


def parse_publish_year(item):
    return item.find_element_by_class_name('date').text


def open_result_item_detail(browser, item):

    former_windows_list = browser.window_handles
    item.find_element_by_class_name('name').find_element_by_tag_name('a').click()
    new_window_name = [item for item in browser.window_handles if item not in former_windows_list][0]
    browser = switch_window_tab(browser, None, new_window_name)  # browser.switch_to.window(new_window_name)

    return browser


def parse_authority_name(browser):

    authorities_list = browser.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[2]/a')

    if len(authorities_list) == 0:
        authorities_list = browser.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[2]/span/a')

    authorities_name_list = [name.text for name in authorities_list]

    return authorities_name_list


def parse_publisher_type(browser):

    publisher_types_list = browser.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/a')
    types_name_list = [item.text for item in publisher_types_list]

    return types_name_list


def open_publisher_info_page(browser):

    # //*[@id="func610"]/div/a
    publisher = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/span/a[1]')
    publisher_name = publisher.text
    publisher.click()

    browser = switch_window_tab(browser)

    return browser, publisher_name


def parse_publisher_complex_factor(browser):

    factor = ""
    try:
        factor = browser.find_element_by_xpath('//*[@id="evaluateInfo"]/li[2]/p[1]/span').text
    except Exception as e:
        pass

    return factor
