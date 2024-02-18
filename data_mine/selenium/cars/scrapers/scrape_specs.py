from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, time
sys.path.insert(0, '../../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *

def scrape_img(driver):
    img_element = driver.find_elements(By.XPATH, '//*[@class="photo-content"]//img')

    if img_element:
        return(img_element[0].get_attribute("src"))
    
    img_element = driver.find_elements(By.XPATH, '/html/body/section/div[2]/div/div[2]/spark-page-section[1]/div/div[2]/picture/img')

    if img_element:
        return(img_element[0].get_attribute("src"))
    
def scrape_specs_1(driver):
    accordions = driver.find_elements(By.CLASS_NAME, "sds-accordion__heading")

    for accordion in accordions:            
        accordion.click()
        accordion.click()

    container_XPATH = "//*[@id='research-trim-specs']"
    category_XPATH = "//h3//span"
    row_header_XPATH = "//td[(@class='row-header')]/strong|//td[(@class='row-content')]"

    container = driver.find_element(By.XPATH, container_XPATH)
    data_elements = container.find_elements(By.XPATH, f"{category_XPATH}|{row_header_XPATH}")

    category = ""
    header = ""
    vehicle = {}
    for element in data_elements:
        if element.tag_name == "span":
            category = element.text
            vehicle[category] = {}
        elif element.tag_name == "strong":
            header = element.text
        else:
            vehicle[category][header] = element.text

    return vehicle

def scrape_specs_2(driver):
    category = ""
    vehicle = {}

    spec_tabs = driver.find_elements(By.XPATH, "//spark-tab")
    for spec_tab in spec_tabs:
        driver.execute_script("arguments[0].click();", spec_tab)        
        category = spec_tab.get_attribute("data-key-spec")
        vehicle[category] = {}
        for spec in driver.find_elements(By.CLASS_NAME, "key-spec"):
            spec_heading = spec.find_element(By.CLASS_NAME, "key-spec-heading")
            spec_value = spec.find_element(By.CLASS_NAME, "key-spec-value")
            highlight(spec_heading, "blue", 5)
            highlight(spec_value, "yellow", 5)

            if (spec_heading.text):
                vehicle[category][spec_heading.text] = spec_value.text

    return vehicle


driver = webdriver.Firefox()

"""

driver.get("https://www.cars.com/research/acura-cl-2003/specs/100352/")
time.sleep(2)
delete_element(driver, By.CLASS_NAME, "global-header-container")
delete_element(driver, By.ID, "onetrust-consent-sdk")
delete_element(driver, By.ID, "credential_picker_container")
print(scrape_specs_1(driver))
print(scrape_img(driver))
"""
driver.get("https://www.cars.com/research/ford-f_150-2024/")
time.sleep(2)
delete_element(driver, By.CLASS_NAME, "global-header-container")
delete_element(driver, By.ID, "onetrust-consent-sdk")
delete_element(driver, By.ID, "credential_picker_container")
print(scrape_specs_2(driver))
#print(scrape_img(driver))
#driver.close()
