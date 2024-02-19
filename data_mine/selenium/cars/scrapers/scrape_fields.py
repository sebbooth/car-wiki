from selenium.webdriver.common.by import By

import sys
sys.path.insert(0, '../../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *

def scrape_fields(driver):
    accordions = driver.find_elements(By.CLASS_NAME, "sds-accordion__heading")

    for accordion in accordions:            
        accordion.click()
        accordion.click()

    container_XPATH = "//*[@id='research-trim-specs']"
    category_XPATH = "//h3//span"
    row_header_XPATH = "//td[(@class='row-header')]/strong|//td[(@class='row-content')]"

    container = driver.find_element(By.XPATH, container_XPATH)
    data_elements = container.find_elements(By.XPATH, f"{category_XPATH}|{row_header_XPATH}")

    fields = {}
    for element in data_elements:
        if element.tag_name == "span":
            category = element.text
            if category == "Exterior" or category == "Interior" or category == "Mechanical" or category == "Entertainment" or category == "Safety":
                pass
            else:
                fields[category] = []
        elif element.tag_name == "strong":
            header = element.text
        else:
            if category == "Exterior" or category == "Interior" or category == "Mechanical" or category == "Entertainment" or category == "Safety":
                pass
            else:
                fields[category].append(header)

    return fields
