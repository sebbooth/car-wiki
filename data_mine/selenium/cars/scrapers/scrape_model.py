from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time

import sys
sys.path.insert(0, '../../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *

from scrape_specs import *

def scrape_model_1(driver):
    specs_link_xpath = '//a[contains(@href, "/specs/")]'
    specs_link = driver.find_element(By.XPATH, specs_link_xpath)
    if specs_link:
        specs_href = specs_link.get_attribute('href')
        driver.get(specs_href)

        change_trim_link = driver.find_elements(By.CLASS_NAME, "change-trim-link")
        if change_trim_link:
            change_trim_link[0].click()

            trim_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'sds-modal__content-body')]//ul//li//a")
            links_dict = {}
            for link in trim_links:
                href = link.get_attribute("href")
                name = link.text
                msrp_span = link.find_element(By.XPATH, ".//following-sibling::span")
                msrp = msrp_span.text.strip()
                links_dict[href] = {"Trim": name, "MSRP": msrp}

            return links_dict
        
def scrape_model_2(driver):
    time.sleep(2)
    delete_element(driver, By.CLASS_NAME, "global-header-container")
    delete_element(driver, By.ID, "onetrust-consent-sdk")
    delete_element(driver, By.ID, "credential_picker_container")

    
    desktop_trim_picker_button = driver.find_element(By.ID, "desktop-trim-picker")
    driver.execute_script("arguments[0].click();", desktop_trim_picker_button)        

    buttons = driver.find_elements(By.XPATH, "//div[@class='popover-picker-main']//button")
    
    trims = []
    for button in buttons:
        highlight(button, "blue", 5)

        button.click()
        print(button.get_attribute("data-option-value"))
        time.sleep(2)

        trim = {"Trim" : button.get_attribute("data-option-value")}    
        trim.update(scrape_specs_2(driver))

        trims.append(trim)
        driver.execute_script("arguments[0].click();", desktop_trim_picker_button)        
        time.sleep(2)

    return trims


if __name__=='__main__':
    options = Options()
    #options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options)

    driver.get("https://www.cars.com/research/acura-cl-2003")
    print(scrape_model_1(driver))

    driver.get("https://www.cars.com/research/kia-ev9-2024/")
    print(scrape_model_2(driver, ))
    driver.close()