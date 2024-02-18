from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import sys
sys.path.insert(0, '../../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *

import time

driver = webdriver.Firefox()
driver.get("https://www.cars.com/research/") 

time.sleep(2)
delete_element(driver, By.CLASS_NAME, "global-header-container")
delete_element(driver, By.ID, "onetrust-consent-sdk")
delete_element(driver, By.ID, "credential_picker_container")

make_select = driver.find_element(By.ID, "make-select")
model_select = driver.find_element(By.ID, "model-select")
year_select = driver.find_element(By.ID, "year-select")
search_button = driver.find_element(By.CLASS_NAME , "js-mmy-search-button")

for make in make_select.find_elements(By.TAG_NAME, "option"):
    make.click()
    
    for model in model_select.find_elements(By.TAG_NAME, "option"):
        model.click()
        
        for year in year_select.find_elements(By.TAG_NAME, "option"):
            year.click()
            
            make_value = make_select.get_attribute("value")
            model_value = model_select.get_attribute("value")
            year_value = year_select.get_attribute("value")

            
            if make_value and model_value and year_value:
                url = f"https://www.cars.com/research/{make_value}-{model_value}-{year_value}"
                make_name = make.text
                model_name = model.text
                year_name = year.text

                vehicle_page = {
                    "Make": make_name,
                    "Model": model_name,
                    "Year": year_name,
                    "URL": url
                }

                write_to_file_json("model_links.txt", [vehicle_page])

driver.quit()
